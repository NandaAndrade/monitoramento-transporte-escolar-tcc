# Levantamento de Requisitos — Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García · **Coorientador:** Frederico Gualberto Ferreira Coelho
**Atividade correspondente:** Atividade 1.1 — Levantamento de Requisitos e Especificação do Sistema (TCC1, 08/2026)

> Este documento consolida os requisitos funcionais e não funcionais do sistema, a partir do que já está definido na [Proposta de TCC1](<Proposta - Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo.pdf>), no [Projeto de TCC](<Projeto de Trabalho de Conclusão de Curso.docx>) e no [resumo da exploração de reconhecimento facial](resumo_reconhecimento_facial_tcc.md), complementado pelas decisões tomadas em conversa com a aluna. Pontos que ainda dependem de definição posterior (Atividades 1.3 e 1.4) estão marcados explicitamente como **em aberto**.

---

## 1. Contexto e escopo

O transporte escolar rural carece de mecanismos automatizados de controle de presença, o que compromete a segurança dos estudantes e a eficiência da gestão pública. O projeto propõe um dispositivo IoT embarcado em ônibus escolares rurais que:

- identifica e registra a presença dos alunos por **reconhecimento facial (vídeo)** e **reconhecimento de voz (áudio)**;
- integra esses dados ao sistema **TRANSCOLAR RURAL**, via rede móvel (MQTT/API);
- gera relatórios estratégicos para gestores escolares e o poder público.

### Escopo por ciclo

| Ciclo | Escopo |
|---|---|
| **TCC1** (este documento) | Levantamento de requisitos, fundamentação teórica (IoT/IA), definição da arquitetura de hardware/software, avaliação de impactos socioeconômicos/legais/ambientais. |
| **TCC2** | Implementação do software embarcado (OpenCV, TensorFlow Lite), integração MQTT/API, simulação controlada, teste piloto em ônibus real, validação de métricas de acurácia/tempo de resposta. |

### Atores / perfis de usuário

| Perfil | Papel no sistema |
|---|---|
| **Gestor escolar / poder público** | Consulta relatórios estratégicos (presença, localização, tempo de viagem, segurança, eficiência operacional, qualidade do serviço). |
| **Administrador do sistema (TI)** | Cadastra alunos e rotas, configura e mantém o dispositivo embarcado, gerencia contas e permissões. |

> **Em aberto:** motoristas/monitores do ônibus e responsáveis pelos alunos foram descartados como perfis com acesso direto ao sistema nesta rodada de definição. Confirmar se isso é intencional (ex.: o motorista não precisa de nenhuma interface local) ou se a interface embarcada precisa de algum retorno visual/sonoro mínimo (ex.: um LED/beep de confirmação de embarque) mesmo sem "perfil de usuário" formal.

---

## 2. Requisitos Funcionais (RF)

### 2.1 Reconhecimento de presença

| ID | Requisito |
|---|---|
| RF-01 | O sistema deve capturar imagem de vídeo do interior do ônibus para identificar os alunos por reconhecimento facial no momento do embarque e do desembarque. |
| RF-02 | O sistema deve capturar áudio para identificar os alunos por reconhecimento de voz, como mecanismo complementar/de reforço ao reconhecimento facial. |
| RF-03 | O sistema deve registrar o evento de presença (aluno, ônibus, rota, horário, tipo de evento — embarque/desembarque) a cada identificação bem-sucedida. |
| RF-04 | O sistema deve emitir um alerta quando ocorrer falha de reconhecimento ou embarque irregular (ex.: aluno não cadastrado, identificação de baixa confiança). |
| RF-05 | O sistema **não deve** persistir a imagem ou o áudio bruto capturado — apenas o resultado do processamento (evento de presença) é armazenado. *(decisão confirmada com a aluna — ver seção 5)* |

### 2.2 Comunicação e integração com o TRANSCOLAR RURAL

| ID | Requisito |
|---|---|
| RF-06 | O sistema deve enviar os eventos de presença ao TRANSCOLAR RURAL em tempo real, via MQTT/API, sempre que houver conectividade de rede móvel disponível. |
| RF-07 | Quando não houver conectividade, o sistema deve armazenar os eventos localmente em uma fila e reenviá-los automaticamente assim que a conexão for reestabelecida (modo híbrido online/offline). |
| RF-08 | O sistema deve garantir que nenhum evento de presença seja perdido ou duplicado entre a captura local e a sincronização com o TRANSCOLAR RURAL. |

### 2.3 Relatórios inteligentes

| ID | Requisito |
|---|---|
| RF-09 | O sistema deve gerar relatório de **presença**: lista de embarque/desembarque e frequência individual por aluno. |
| RF-10 | O sistema deve gerar relatório de **localização**: verificação de embarque/desembarque nos pontos corretos da rota. |
| RF-11 | O sistema deve gerar relatório de **tempo de viagem**: comparação entre tempo planejado e tempo real de cada rota. |
| RF-12 | O sistema deve gerar relatório de **segurança**: alertas de embarque irregular ou falha de reconhecimento. |
| RF-13 | O sistema deve gerar relatório de **eficiência operacional**: custo por aluno/km e identificação de rotas subutilizadas. |
| RF-14 | O sistema deve gerar relatório de **qualidade do serviço**, incluindo indicadores como ranking de rotas. |
| RF-15 | Os relatórios devem estar disponíveis para consulta pelo perfil de Gestor escolar / poder público. |

### 2.4 Administração e cadastro

| ID | Requisito |
|---|---|
| RF-16 | O administrador do sistema deve poder cadastrar, editar e remover alunos, associando-os a uma rota e a um ônibus específico. |
| RF-17 | O administrador do sistema deve poder cadastrar e configurar rotas e ônibus (pontos de embarque/desembarque, horários planejados). |
| RF-18 | O administrador do sistema deve poder gerenciar o cadastro biométrico de referência de cada aluno (amostra facial/voz usada para comparação), incluindo atualização e remoção. |
| RF-19 | O administrador do sistema deve poder configurar e monitorar remotamente o dispositivo embarcado (status, versão de software, conectividade). |

---

## 3. Requisitos Não Funcionais (RNF)

### 3.1 Desempenho e escala

| ID | Requisito |
|---|---|
| RNF-01 | O sistema deve suportar o reconhecimento de até **~20 alunos por ônibus**, no cenário do piloto de 1 ônibus (TCC2). *(suposição de dimensionamento — ver seção 5)* |
| RNF-02 | O reconhecimento facial/de voz de um aluno deve ocorrer dentro de uma latência máxima aceitável para o fluxo de embarque, a ser definida na Atividade 1.3 com base no hardware escolhido. *(valor numérico ainda em aberto — ver seção 5)* |
| RNF-03 | A acurácia do reconhecimento de presença deve ser **superior a 90%**, conforme meta definida na proposta do projeto. |

### 3.2 Confiabilidade e disponibilidade

| ID | Requisito |
|---|---|
| RNF-04 | O sistema deve continuar registrando eventos de presença localmente mesmo na ausência total de conectividade de rede (modo offline), sem perda de dados. |
| RNF-05 | O dispositivo embarcado deve ser tolerante a condições reais de operação: vibração do veículo, iluminação variável, ângulos de câmera não controlados. |
| RNF-06 | O sistema deve informar de forma auditável (log) falhas de hardware, falhas de reconhecimento e falhas de sincronização. |

### 3.3 Privacidade e conformidade legal (LGPD)

| ID | Requisito |
|---|---|
| RNF-07 | O sistema não deve armazenar imagem ou áudio bruto dos alunos — apenas dados derivados necessários à verificação de presença (ex.: template/embedding biométrico de referência, cadastrado com consentimento). |
| RNF-08 | O tratamento de dados biométricos de menores de idade deve seguir as exigências da LGPD, incluindo base legal e consentimento dos responsáveis — a ser detalhado na Atividade 1.4. |
| RNF-09 | O acesso a dados de presença e a cadastros de alunos deve ser restrito por perfil (controle de acesso), disponível apenas ao Administrador do sistema e ao Gestor escolar. |
| RNF-10 | Os dados de referência biométrica devem ser armazenados de forma protegida (ex.: criptografados em repouso), tanto localmente no dispositivo quanto no backend do TRANSCOLAR RURAL. |

### 3.4 Hardware e energia

| ID | Requisito |
|---|---|
| RNF-11 | O dispositivo embarcado deve operar com alimentação compatível com a rede elétrica veicular do ônibus escolar. |
| RNF-12 | O hardware embarcado (Raspberry Pi vs. ESP32, câmera HD, microfone direcional) será definido via análise de trade-off na Atividade 1.3, considerando custo, capacidade de processamento e viabilidade de embarque dos modelos de reconhecimento. |
| RNF-13 | O software de reconhecimento deve ser compatível com execução em borda (edge computing), sem depender de processamento em nuvem para a etapa de identificação. |

### 3.5 Manutenibilidade e portabilidade

| ID | Requisito |
|---|---|
| RNF-14 | O software deve ser desenvolvido em Python, utilizando OpenCV e TensorFlow Lite, de forma modular para permitir substituição futura dos modelos de reconhecimento. |
| RNF-15 | O dispositivo deve poder ser atualizado remotamente (software) pelo Administrador do sistema. |

---

## 4. Restrições

- **RC-01** — Dados de alunos menores de idade não podem ser usados em nenhuma fase de prototipagem/teste antes da formalização legal (Atividade 1.4); os testes atuais usam apenas datasets públicos de adultos (LFW, AT&T/Olivetti — ver [resumo_reconhecimento_facial_tcc.md](resumo_reconhecimento_facial_tcc.md)).
- **RC-02** — O banco de dados para armazenamento local/sincronização será PostgreSQL ou Firebase, a decidir na Atividade 1.3.
- **RC-03** — O sistema deve se integrar ao TRANSCOLAR RURAL, sistema já existente e externo ao escopo deste projeto — sua especificação técnica (API/contrato de dados) precisa ser obtida junto ao responsável pelo TRANSCOLAR RURAL (ver pendência na seção 5).
- **RC-04** — Ambiente de operação real: interior de ônibus escolar rural, com possível instabilidade de conectividade 4G/5G.

---

## 5. Questões em aberto

Itens que não puderam ser totalmente resolvidos com a documentação existente e as respostas já obtidas, e que devem ser fechados até a conclusão da Atividade 1.1 ou nas Atividades 1.3/1.4:

1. **Especificação técnica do TRANSCOLAR RURAL** — a proposta cita repetidamente a integração com o TRANSCOLAR RURAL, mas não há, nos arquivos do repositório, nenhuma documentação sobre a API/formato de dados/protocolo desse sistema. Isso é necessário para detalhar RF-06 a RF-08. Existe contato/documentação técnica disponível (ex.: responsável pelo TRANSCOLAR RURAL, órgão público)?
2. **Latência máxima tolerada (RNF-02)** — a proposta menciona explicitamente que essa métrica "será mapeada" na Atividade 1.1, mas nenhum valor numérico foi definido ainda. Há uma referência (ex.: tempo de embarque médio de um aluno na porta do ônibus) que ajude a estimar um valor razoável (ex.: <2s, <5s)?
3. **Papel do motorista/monitor no fluxo** — ficou definido que motorista/monitor e responsáveis não terão acesso ao sistema como "perfil de usuário", mas fisicamente alguém opera o ônibus durante o embarque. O dispositivo precisa dar algum feedback local (luz/som) confirmando o reconhecimento, mesmo sem tela/login?
4. **Retenção dos eventos de presença** — ainda que o vídeo/áudio bruto não seja armazenado (RF-05/RNF-07), por quanto tempo os eventos de presença (dado derivado: "aluno X embarcou às 7h14") devem ficar retidos no dispositivo e no TRANSCOLAR RURAL?
5. **Consentimento dos responsáveis** — o cadastro biométrico de referência (RF-18) pressupõe consentimento formal dos responsáveis pelo aluno. O fluxo de obtenção/registro desse consentimento faz parte do escopo deste sistema (ex.: uma tela de opt-in) ou é tratado fora do sistema (processo administrativo da escola)?
6. **Hardware e banco de dados definitivos** — Raspberry Pi vs. ESP32 e PostgreSQL vs. Firebase seguem como decisões da Atividade 1.3; os requisitos acima foram escritos de forma a não depender dessa escolha, mas RNF-02, RNF-11 e RNF-12 precisarão de números concretos assim que a decisão for tomada.

---

## 6. Rastreabilidade com os objetivos da proposta

| Objetivo específico (proposta) | Requisitos relacionados |
|---|---|
| Desenvolver protótipo de hardware IoT com câmera e microfone | RNF-11, RNF-12, RC-04 |
| Implementar algoritmos de reconhecimento facial e de voz | RF-01, RF-02, RF-03, RNF-03, RNF-13, RNF-14 |
| Integrar o dispositivo ao TRANSCOLAR RURAL via rede móvel | RF-06, RF-07, RF-08, RC-03 |
| Criar relatórios inteligentes para gestores escolares | RF-09 a RF-15 |
| Avaliar desempenho, segurança e confiabilidade do sistema | RNF-01 a RNF-06, RNF-09, RNF-10 |
