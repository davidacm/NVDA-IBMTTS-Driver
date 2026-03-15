# -*- coding: UTF-8 -*-
#Copyright (C) 2026 David CM, released under the GPL.
# Author: David CM <dhf360@gmail.com> and others.
#synthDrivers/_fakeEci.py

import struct
from ._ipc import IBMTTSClient, HostIds, SharedMemory, launch_host_32

class EciDLL:
    def __init__(self, dll_path, etidev_path=None):
        launch_host_32()
        self._client = IBMTTSClient()
        self._client.connect()
        self._shm = None       
        self._callback = None
        if etidev_path:
            self.eciLoadEtidev(etidev_path)
        self.eciLoadLibrary(dll_path)

    def eciLoadLibrary(self, path):
        return self._client.call(HostIds.LOAD_LIBRARY, path)

    def eciLoadEtidev(self, path):
        return self._client.call(HostIds.LOAD_ETIDEV, path)

    def eciVersion(self):
        return self._client.call(HostIds.ECI_VERSION)

    def eciNew(self):
        return self._client.call(HostIds.ECI_NEW)

    def eciNewEx(self, dialect):
        return self._client.call(HostIds.ECI_NEW_EX, dialect)

    def eciDelete(self, handle):
        if self._shm:
            self._shm.stop()
            self._shm = None
        return self._client.call(HostIds.ECI_DELETE, handle)

    def eciRegisterCallback(self, handle, callback_func, _=None):
        self._callback = callback_func
        return 1

    def eciSetOutputBuffer(self, handle, samples):
        if not self._callback:
            raise ValueError("Callback function must be registered before setting output buffer.")
        if self._shm:
            self._shm.stop()
        self._client.call(HostIds.SET_BUFFER, handle, samples)
        self._shm = SharedMemory(handle, samples, self._callback)
        return 1

    def eciGetAvailableLanguages(self):
        res = self._client.call(HostIds.ECI_GET_AVAILABLE_LANGUAGES)
        if isinstance(res, bytes):
            count = struct.unpack("<i", res[:4])[0]
            if count <= 0: return []
            return list(struct.unpack(f"<{count}i", res[4:]))
        return []

    # --- Passthrough functions ---

    def eciAddText(self, handle, text):
        return self._client.call(HostIds.ECI_ADD_TEXT, handle, text)

    def eciInsertIndex(self, handle, index):
        return self._client.call(HostIds.ECI_INSERT_INDEX, handle, index)

    def eciSynthesize(self, handle):
        return self._client.call(HostIds.ECI_SYNTHESIZE, handle)

    def eciStop(self, handle):
        return self._client.call(HostIds.ECI_STOP, handle)

    def eciGetParam(self, handle, param_id):
        return self._client.call(HostIds.ECI_GET_PARAM, handle, param_id)

    def eciSetParam(self, handle, param_id, value):
        return self._client.call(HostIds.ECI_SET_PARAM, handle, param_id, value)

    def eciGetVoiceParam(self, handle, voice_id, param_id):
        return self._client.call(HostIds.ECI_GET_VOICE_PARAM, handle, voice_id, param_id)

    def eciSetVoiceParam(self, handle, voice_id, param_id, value):
        return self._client.call(HostIds.ECI_SET_VOICE_PARAM, handle, voice_id, param_id, value)

    def eciCopyVoice(self, handle, from_idx, to_idx):
        return self._client.call(HostIds.ECI_COPY_VOICE, handle, from_idx, to_idx)

    def eciNewDict(self, handle):
        return self._client.call(HostIds.ECI_NEW_DICT, handle)

    def eciLoadDict(self, handle, dict_handle, dict_vol, filename):
        return self._client.call(HostIds.ECI_LOAD_DICT, handle, dict_handle, dict_vol, filename)

    def eciSetDict(self, handle, dict_handle):
        return self._client.call(HostIds.ECI_SET_DICT, handle, dict_handle)

    def get_audio_buffer_ptr(self):
        if self._shm:
            return self._shm.get_audio_buffer_ptr()
        return None
    