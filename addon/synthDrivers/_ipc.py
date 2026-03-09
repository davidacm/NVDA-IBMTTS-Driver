# -*- coding: UTF-8 -*-
#Copyright (C) 2026 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/_ipc.py

import ctypes
from ctypes import wintypes, byref
import threading
import subprocess
import os
import time

process_host32 = None
PIPE_NAME = r"\\.\pipe\ibmtts_host32"
PIPE_SIZE = 65536


GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
ERROR_PIPE_BUSY = 231
PIPE_READMODE_MESSAGE = 0x00000002

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Additional Win32 APIs for shared memory + event
OpenFileMappingW = kernel32.OpenFileMappingW
OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
OpenFileMappingW.restype = wintypes.HANDLE

MapViewOfFile = kernel32.MapViewOfFile
MapViewOfFile.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
MapViewOfFile.restype = wintypes.LPVOID

UnmapViewOfFile = kernel32.UnmapViewOfFile
UnmapViewOfFile.argtypes = [wintypes.LPCVOID]
UnmapViewOfFile.restype = wintypes.BOOL

OpenEventW = kernel32.OpenEventW
OpenEventW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
OpenEventW.restype = wintypes.HANDLE

WaitForSingleObject = kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
WaitForSingleObject.restype = wintypes.DWORD

INFINITE = 0xFFFFFFFF
FILE_MAP_WRITE = 0x0002
FILE_MAP_READ = 0x0004
SYNCHRONIZE = 0x00100000
CloseHandle = kernel32.CloseHandle
WaitNamedPipeW = kernel32.WaitNamedPipeW
WaitNamedPipeW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
WaitNamedPipeW.restype = wintypes.BOOL

# Host process handle functions

def terminate_host_32():
    global process_host32
    if process_host32:
        try:
            process_host32.terminate()
            process_host32.wait(timeout=1.0)
        except Exception:
            try:
                process_host32.kill()
            except:
                pass
        finally:
            process_host32 = None

def launch_host_32(dll_filename="ibmtts_host32.dll", timeout=5.0):
    """
    Launch the 32-bit host and wait for the Pipe to become available.
    """
    global process_host32
    pid = os.getpid()
    
    # If there is already one, we try not to launch another (the Mutex in host will still protect)
    if process_host32 and process_host32.poll() is None:
        return process_host32

    base_path = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.join(base_path, dll_filename)
    
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"Host DLL not found in: {dll_path}")

    system_root = os.environ.get('SystemRoot', 'C:\\Windows')
    rundll32 = os.path.join(system_root, 'SysWOW64', 'rundll32.exe')
    if not os.path.exists(rundll32):
        rundll32 = os.path.join(system_root, 'System32', 'rundll32.exe')
    cmd = f'{rundll32} "{dll_path}",StartHost {pid}'
    process_host32 = subprocess.Popen(
        cmd, 
        creationflags=0x08000000, 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )

    # Pipe Polling
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        # We check if the pipe exists and is ready
        if WaitNamedPipeW(PIPE_NAME, 100):
            return process_host32
        
        # If the process died at startup (e.g. failed to load ibmeci.dll)
        if process_host32.poll() is not None:
            exit_code = process_host32.returncode
            process_host32 = None
            raise RuntimeError(f"The 32-bit host ended abruptly.code: {exit_code}")
        time.sleep(0.1)
    terminate_host_32()
    raise TimeoutError("The host Pipe did not appear after the timeout.")

def pack(id: int, *args):
    """
    Pack data according to the protocol.
    
    Args:
        id (int): u16 function ID
        *args: Mix of integers and strings
            - int: packed as 4 bytes (little-endian)
            - str: packed as offset to string location (4 bytes), 
                   actual string appended at end (UTF-8 null-terminated)
    
    Returns:
        bytes: Packed message payload (id + args + strings)
    
    Example:
        pack(2, 9, "hello", 4) → b'\x02\x00\x09\x00\x00\x00\x0e\x00\x00\x00\x04\x00\x00\x00hello\x00'
    """

    if len(args) == 1 and isinstance(args[0], str):
        return id.to_bytes(2, "little", signed=False) + args[0].encode('utf-8') + b'\x00'

    # Start with the ID (2 bytes, little-endian)
    payload = id.to_bytes(2, "little", signed=False)
    
    # Calculate where strings will start
    string_start = 2 + (len(args) * 4)

    string_data = b''
    for arg in args:
        if isinstance(arg, bytes):
            # Write the offset where this string will be located
            payload += (string_start + len(string_data)).to_bytes(4, "little", signed=False)
            # Prepare the string data (UTF-8 encoded, null-terminated)
            string_data += arg + b'\x00'
        elif isinstance(arg, int):
            # Write the integer as 4 bytes (little-endian)
            payload += arg.to_bytes(4, "little", signed=True)
        else:
            raise TypeError(f"Unsupported argument type: {type(arg).__name__}")
    
    # Append all strings
    payload += string_data
    
    return payload

def parse_response(data: bytes):
    """
    Parse a response message according to the protocol.
    
    Args:
        data (bytes): Raw response data (length-prefixed)
    the first byte determines the data of the response.
    0 = signed int
    1 = unsigned int
    2 = 0 ended byte string
    3 = utf-8 string
    4 = Host error (string)
    the rest of bytes are the parsed data.
    Returns: an int or byte string.
    """
    if len(data) < 1:
        raise ValueError("Response data is too short to contain type information")
    
    resp_type = data[0]
    resp_data = data[1:]
    match resp_type:
        case 0:  # signed int
            return int.from_bytes(resp_data, "little", signed=True)
        case 1:  # unsigned int
            return int.from_bytes(resp_data, "little", signed=False)
        case 2:  # byte string
            return resp_data
        case 3: # utf-8 string
            return resp_data.decode('utf-8', errors='ignore')
        case 4: # error string
            raise Exception("Host error", resp_data.decode('utf-8', errors='ignore'))
        case _:
            raise ValueError(f"Unknown response type: {resp_type}")



class HostIds:
    LOAD_LIBRARY = 1
    ECI_VERSION = 2
    ECI_NEW = 3
    ECI_NEW_EX = 4
    SET_BUFFER = 5
    ECI_ADD_TEXT = 6
    ECI_INSERT_INDEX = 7
    ECI_SYNTHESIZE = 8
    ECI_GET_AVAILABLE_LANGUAGES = 9
    ECI_STOP = 10
    ECI_GET_PARAM = 11
    ECI_SET_PARAM = 12
    ECI_GET_VOICE_PARAM = 13
    ECI_SET_VOICE_PARAM = 14
    ECI_COPY_VOICE = 15
    ECI_NEW_DICT = 16
    ECI_LOAD_DICT = 17
    ECI_SET_DICT = 18
    ECI_DELETE = 19


class IBMTTSClient:
    def __init__(self, pipe_name=PIPE_NAME):
        self.pipe_name = pipe_name
        self.h_pipe = None

    def connect(self):
        while True:
            self.h_pipe = kernel32.CreateFileW(
                self.pipe_name, GENERIC_READ | GENERIC_WRITE,
                0, None, OPEN_EXISTING, 0, None
            )
            if self.h_pipe != -1:
                break
            
            err = kernel32.GetLastError()
            if err != 231: # ERROR_PIPE_BUSY
                raise ConnectionError(f"unable to connect to the pipe. Error: {err}")
            kernel32.WaitNamedPipeW(self.pipe_name, 2000)

    def _send_request(self, data: bytes) -> bytes:
        """
        Sends a message and receives a response using atomic Message Mode.
        No length-prefixing required.
        """
        written = wintypes.DWORD(0)
        # 1. Write the message. In Message Mode, this is sent as a single unit.
        if not kernel32.WriteFile(self.h_pipe, data, len(data), ctypes.byref(written), None):
            raise OSError(kernel32.GetLastError(), "WriteFile failed")

        # 2. Read the response. 
        # Because the pipe is in PIPE_READMODE_MESSAGE, ReadFile will wait until 
        # a complete message is available and return only that message.
        buf = ctypes.create_string_buffer(PIPE_SIZE)
        read = wintypes.DWORD(0)
        
        if not kernel32.ReadFile(self.h_pipe, buf, PIPE_SIZE, ctypes.byref(read), None):
            err = kernel32.GetLastError()
            # ERROR_MORE_DATA (234) means the message was larger than 64KB
            raise OSError(err, "ReadFile failed")
        # Return exactly the number of bytes read for this message
        return buf.raw[:read.value]

    def call(self, func_id: int, *args):
        """Send a request and wait for the response."""
        return parse_response(self._send_request(pack(func_id, *args)))

class ECICallbackReturn:
    eciDataNotProcessed = 0
    eciDataProcessed = 1
    eciDataAbort = 2

class SharedHeader(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("eciHandle", wintypes.DWORD),
        ("msg", wintypes.DWORD),
        ("lparam", wintypes.LONG),
    ]

class SharedMemory:
    def __init__(self, eci_id, samples_capacity, external_callback):
        self.eci_id = eci_id
        self.total_size = (samples_capacity * 2) + 12
        self.external_callback = external_callback
        
        self.shm_name = f"Local\\eci_shm_{eci_id:x}"
        self.evt_ready_name = f"Local\\eci_ready_{eci_id:x}"
        self.evt_proc_name = f"Local\\eci_proc_{eci_id:x}"
        self.h_map = None
        self.view = None
        self._h_evt_ready = None
        self.h_evt_proc = None
        self.header = None

        self._stop_event = kernel32.CreateEventW(None, True, False, None)
        self._open_resources()
        self._thread = threading.Thread(target=self._worker_loop, name=f"ECI_Audio_{eci_id:x}", daemon=True)
        self._thread.start()

    def _worker_loop(self):
        handles = (wintypes.HANDLE * 2)(self._stop_event, self._h_evt_ready)
        try:
            while True:
                res = kernel32.WaitForMultipleObjects(2, byref(handles), False, INFINITE)
                if res == 0: # stop thread
                    break
                elif res == 1: # host pipe event
                    # 1. header
                    handle = self.header.eciHandle
                    msg = self.header.msg
                    lparam = self.header.lparam
                    return_val = self.external_callback(handle, msg, lparam, 0)
                    self.header.eciHandle = return_val
                    kernel32.SetEvent(self.h_evt_proc)
        except Exception as e:
            raise(f"[!] Critical error in shared memory thread {self.eci_id:x}: {e}")
        finally:
            self._cleanup()

    def _open_resources(self):
        self.h_map = OpenFileMappingW(FILE_MAP_WRITE, False, self.shm_name)
        if not self.h_map: raise OSError(ctypes.get_last_error(), "SHM not found")
        self.view = MapViewOfFile(self.h_map, FILE_MAP_WRITE, 0, 0, self.total_size)
        if not self.view: raise OSError(ctypes.get_last_error(), "MapViewOfFile failed")

        self.header = SharedHeader.from_address(self.view)
        self._h_evt_ready = OpenEventW(SYNCHRONIZE | 0x0002, False, self.evt_ready_name)
        self.h_evt_proc = OpenEventW(SYNCHRONIZE | 0x0002, False, self.evt_proc_name)

    def get_audio_buffer_ptr(self):
        """Public access to audio pointer (byte 12)"""
        if not self.view: return None
        return self.view + 12

    def stop(self):
        kernel32.SetEvent(self._stop_event)

    def _cleanup(self):
        if self.view: UnmapViewOfFile(self.view)
        if self.h_map: CloseHandle(self.h_map)
        if self._h_evt_ready: CloseHandle(self._h_evt_ready)
        if self.h_evt_proc: CloseHandle(self.h_evt_proc)
