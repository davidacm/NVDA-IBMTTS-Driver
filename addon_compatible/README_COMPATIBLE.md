# NVDA IBMTTS Driver - Versão Compatível (32-bit e 64-bit)

## Estrutura Criada

Este diretório `addon_compatible` contém uma versão do IBMTTS Driver que suporta tanto NVDA 32-bit (< 2026.1) quanto NVDA 64-bit (>= 2026.1).

```
addon_compatible/
├── synthDrivers/
│   ├── ibmeci.py              # Dispatcher principal (decide qual versão carregar)
│   ├── _ibmeci32.py           # Implementação 32-bit (NVDA < 2026.1)
│   ├── _ibmeci32Impl.py       # ctypes wrapper 32-bit
│   ├── _ibmeci64.py           # Implementação 64-bit proxy (NVDA >= 2026.1)
│   ├── _settingsDB32.py       # Configurações para 32-bit
│   ├── _settingsDB64.py       # Configurações para 64-bit
│   ├── _configHelper32.py     # Helper de configuração 32-bit
│   └── _configHelper64.py     # Helper de configuração 64-bit
├── _synthDrivers32/           # Código 32-bit para synthDriverHost32
│   ├── ibmeci.py
│   ├── _ibmeci.py
│   ├── _settingsDB.py
│   └── _configHelper.py
├── globalPlugins/
│   ├── ibmtts.py              # Painel de configurações (com detecção de arquitetura)
│   └── _ibmttsUtils.py
├── doc/                        # Documentação
├── locale/                     # Traduções
├── manifest.ini                # Manifesto do addon
└── installTasks.py             # Tarefas de instalação
```

## Como Funciona

### Dispatcher (ibmeci.py)

O arquivo principal `synthDrivers/ibmeci.py` atua como um dispatcher:

1. **Detecta a versão do NVDA** - Lê `globalVars.nvdaVersion`
2. **Verifica synthDriverHost32** - Confere se o bridge está disponível
3. **Carrega a implementação apropriada**:
   - **NVDA >= 2026.1 (64-bit)**: Carrega `_ibmeci64.py` (usa SynthDriverProxy32)
   - **NVDA < 2026.1 (32-bit)**: Carrega `_ibmeci32.py` (usa ctypes diretamente)

### Arquiteturas

#### 32-bit (NVDA < 2026.1)
- Usa `_ibmeci32.py` que importa `_ibmeci32Impl.py` (ctypes wrapper)
- Carrega DLLs 32-bit diretamente via `ctypes.windll.LoadLibrary()`
- Usa `_settingsDB32.py` e `_configHelper32.py`

#### 64-bit (NVDA >= 2026.1)
- Usa `_ibmeci64.py` que herda de `SynthDriverProxy32`
- Comunica-se com processo 32-bit via `synthDriverHost32`
- O código 32-bit roda em `_synthDrivers32/` (processo isolado)
- Usa `_settingsDB64.py` e `_configHelper64.py`

## Compatibilidade

| Versão NVDA | Arquitetura | Implementação | Status |
|-------------|-------------|---------------|--------|
| 2019.3 - 2024.4 | 32-bit | _ibmeci32.py | ✅ Suportado |
| 2025.1 - 2026.0 | 32-bit | _ibmeci32.py | ✅ Suportado |
| 2026.1+ | 64-bit | _ibmeci64.py + synthDriverHost32 | ✅ Suportado |

## Instalação

1. Compacte o diretório `addon_compatible` como `.nvda-addon`
2. Instale no NVDA através do Gerenciador de Add-ons
3. O dispatcher selecionará automaticamente a implementação correta

## Notas Importantes

- O diretório `_synthDrivers32/` deve estar no nível do addon (ao lado de `synthDrivers/`)
- As configurações são compartilhadas entre as duas versões
- O `globalPlugins/ibmtts.py` detecta a arquitetura para importar o config correto
- Para testar, use NVDA 2026.1 alpha/beta para a versão 64-bit

## Créditos

- David CM <dhf360@gmail.com> - Autor original
- x0 e outros - Contribuidores
- Wendrill Accenow Brandão - Traduções português BR/PT
- Adaptado para compatibilidade 32/64-bit em 2025
