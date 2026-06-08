# 🔥 TITAN ADB PRO ULTRA - FINAL EDITION 🔥

Uma interface gráfica moderna e completa para controlar dispositivos Android via ADB.

## 📋 Recursos

✅ **Explorador de Arquivos** - Navegue pelo sistema de arquivos do Android
✅ **Shell ADB** - Execute comandos shell diretamente
✅ **Gerenciador de Apps** - Liste, instale e desinstale aplicativos
✅ **Apps Rodando** - Veja processos em execução e finalize-os
✅ **Gerenciador de Permissões** - Conceda ou revogue permissões
✅ **Monitor** - Monitore CPU e recursos do dispositivo
✅ **Automação** - Gamer Mode, Force Stop de apps
✅ **Espelhamento** - Controle remoto do dispositivo via Scrcpy
✅ **Screenshots** - Capture telas do dispositivo

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- ADB instalado e configurado
- Scrcpy (opcional, para espelhamento)

### Setup

```bash
pip install -r requirements.txt
python main.py
```

## 📁 Estrutura do Projeto

```
TITAN-ADB-PRO/
├── main.py              # Arquivo principal
├── config.py            # Configurações globais
├── utils.py             # Funções utilitárias
├── requirements.txt     # Dependências
├── README.md            # Este arquivo
└── tabs/                # Módulo com as abas
    ├── __init__.py
    ├── explorer_tab.py
    ├── shell_tab.py
    ├── apps_tab.py
    ├── running_tab.py
    ├── manage_tab.py
    ├── perms_tab.py
    ├── monitor_tab.py
    └── auto_tab.py
```

## 🎮 Como Usar

1. **Conectar ao dispositivo**
   - USB: Clique em "ADB USB"
   - WiFi: Insira IP:Porta e clique em "Conectar"

2. **Navegar pelas abas**
   - Cada aba tem uma função específica

3. **Controle Remoto**
   - Ative o botão "CONTROLE REMOTO"
   - Seus cliques do mouse serão enviados ao dispositivo

---

**Desenvolvido com ❤️ para geeks do Android**
