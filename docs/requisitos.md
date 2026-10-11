# Levantamento de Requisitos — Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García · **Coorientador:** Frederico Gualberto Ferreira Coelho
**Atividade correspondente:** Atividade 1.1 — Levantamento de Requisitos e Especificação do Sistema (TCC1, 08/2026)

> Este documento consolida os requisitos funcionais e não funcionais do sistema, a partir do que já está definido na [Proposta de TCC1](proposta/proposta_tcc1.pdf), no [Projeto de TCC](proposta/projeto_tcc.docx) e no [resumo da exploração de reconhecimento facial](estudo_reconhecimento_facial.md), complementado pelas decisões tomadas em conversa com a aluna. Pontos que ainda dependem de definição posterior (Atividades 1.3 e 1.4) estão marcados explicitamente como **em aberto**.

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

> **Decidido:** motoristas/monitores do ônibus e responsáveis pelos alunos não são perfis com acesso ao sistema (sem tela, login ou interface de consulta). O motorista/monitor, porém, recebe um **retorno local mínimo** do dispositivo durante o embarque — LED e sinal sonoro de confirmação ou falha de reconhecimento (ver RF-20). Os responsáveis participam apenas indiretamente, por meio do consentimento coletado pela escola e registrado pelo Administrador (ver RF-21).

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
| RF-20 | O dispositivo embarcado deve fornecer retorno local imediato a cada tentativa de identificação: **LED verde + bipe curto** para aluno reconhecido e **LED vermelho + bipe duplo** para falha de reconhecimento ou aluno não cadastrado, permitindo ao motorista/monitor agir sem precisar de tela ou login. |

### 2.2 Comunicação e integração com o TRANSCOLAR RURAL

| ID | Requisito |
|---|---|
| RF-06 | O sistema deve enviar os eventos de presença ao TRANSCOLAR RURAL em tempo real, via MQTT/API, sempre que houver conectividade de rede móvel disponível. *(formato e protocolo exatos dependem da especificação do TRANSCOLAR RURAL — ver seção 5)* |
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
| RF-18 | O administrador do sistema deve poder gerenciar o cadastro biométrico de referência de cada aluno (amostra facial/voz usada para comparação), incluindo atualização e remoção. O cadastro só pode ser realizado após o registro do consentimento do responsável (RF-21). |
| RF-19 | O administrador do sistema deve poder configurar e monitorar remotamente o dispositivo embarcado (status, versão de software, conectividade). |
| RF-21 | O administrador do sistema deve registrar, para cada aluno, o recebimento do consentimento formal do responsável (data, responsável que consentiu e responsável pelo registro). A coleta do consentimento em si é um processo administrativo da escola, **fora do sistema**. O sistema deve impedir o cadastro biométrico sem consentimento registrado e, em caso de revogação, deve remover a referência biométrica do aluno no backend e nos dispositivos. |

---

## 3. Requisitos Não Funcionais (RNF)

### 3.1 Desempenho e escala

| ID | Requisito |
|---|---|
| RNF-01 | O sistema deve suportar o reconhecimento de até **~20 alunos por ônibus**, no cenário do piloto de 1 ônibus (TCC2). *(suposição de dimensionamento — ver seção 5)* |
| RNF-02 | O reconhecimento de um aluno — da detecção do rosto na câmera até o retorno local (RF-20) — deve ocorrer em **no máximo 2 segundos**, para não formar fila na porta do ônibus. No benchmark preliminar em PC, o tempo médio de comparação por par foi de 0,09 s (SFace) e 0,74 s (ArcFace); o valor deve ser revalidado no hardware embarcado escolhido na Atividade 1.3. |
| RNF-03 | A acurácia do reconhecimento de presença deve ser **superior a 90%**, conforme meta definida na proposta do projeto. Entre os dois tipos de erro, **registrar o aluno errado (falso positivo) é o mais grave**: o limiar de decisão deve priorizar a precisão, mesmo à custa de recall. |

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
| RNF-16 | Retenção dos eventos de presença (dados derivados): **no dispositivo**, o evento fica guardado só até o envio ao backend ser confirmado e é apagado logo em seguida (minimização de dados); **no backend**, os eventos ficam guardados durante o ano letivo corrente e mais 1 ano, para relatórios e prestação de contas, e depois são eliminados ou anonimizados. Os prazos devem ser confirmados na análise legal da Atividade 1.4. |

### 3.4 Hardware e energia

| ID | Requisito |
|---|---|
| RNF-11 | O dispositivo embarcado deve operar com alimentação compatível com a rede elétrica veicular do ônibus escolar. |
| RNF-12 | O hardware embarcado (Raspberry Pi vs. ESP32, câmera HD, microfone direcional) será definido via análise de trade-off na Atividade 1.3, considerando custo, capacidade de processamento e viabilidade de embarque dos modelos de reconhecimento. *(tendência atual: Raspberry Pi 5 + AI HAT com Hailo-10 — ver seção 5)* |
| RNF-13 | O software de reconhecimento deve ser compatível com execução em borda (edge computing), sem depender de processamento em nuvem para a etapa de identificação. |

### 3.5 Manutenibilidade e portabilidade

| ID | Requisito |
|---|---|
| RNF-14 | O software deve ser desenvolvido em Python, utilizando OpenCV e TensorFlow Lite, de forma modular para permitir substituição futura dos modelos de reconhecimento. |
| RNF-15 | O dispositivo deve poder ser atualizado remotamente (software) pelo Administrador do sistema. |

---

## 4. Restrições

- **RC-01** — Dados de alunos menores de idade não podem ser usados em nenhuma fase de prototipagem/teste antes da formalização legal (Atividade 1.4); os testes atuais usam apenas datasets públicos de adultos (LFW, AT&T/Olivetti — ver [estudo_reconhecimento_facial.md](estudo_reconhecimento_facial.md)).
- **RC-02** — O banco de dados para armazenamento local/sincronização será PostgreSQL ou Firebase, a decidir na Atividade 1.3.
- **RC-03** — O sistema deve se integrar ao TRANSCOLAR RURAL, sistema já existente e externo ao escopo deste projeto — sua especificação técnica (API/contrato de dados) precisa ser obtida junto ao responsável pelo TRANSCOLAR RURAL (ver pendência na seção 5).
- **RC-04** — Ambiente de operação real: interior de ônibus escolar rural, com possível instabilidade de conectividade 4G/5G.

---

## 5. Questões em aberto

### 5.1 Questões resolvidas (05/10/2026 e 11/10/2026)

| Questão | Decisão | Requisitos afetados |
|---|---|---|
| Latência máxima tolerada | ≤ 2 s por aluno, da detecção ao retorno local; revalidar no hardware embarcado | RNF-02 |
| Papel do motorista/monitor | Sem perfil de usuário, mas o dispositivo dá retorno local por LED + bipe (confirmação/falha) | RF-20, seção 1 |
| Retenção dos eventos de presença | Dispositivo: só até o envio ser confirmado. Backend: ano letivo corrente + 1 ano, depois elimina ou anonimiza | RNF-16 |
| Consentimento dos responsáveis | Coleta fora do sistema (processo da escola). O sistema registra o consentimento, bloqueia o cadastro biométrico sem ele e trata a revogação | RF-18, RF-21 |
| Erro mais grave no reconhecimento (11/10) | Registrar o aluno errado (falso positivo) é pior do que deixar de registrar um aluno (falso negativo). O limiar de cada modelo deve ser calibrado priorizando a precisão | RNF-03 |
| Escopo do reconhecimento de voz (11/10) | No TCC I, a voz entra só na revisão bibliográfica. A seleção e a avaliação do modelo de locutor ficam para o TCC II | RF-02 |

### 5.2 Questões ainda em aberto

1. **Especificação técnica do TRANSCOLAR RURAL** — não há, nos arquivos do repositório, documentação sobre a API, o formato de dados ou o protocolo desse sistema, e ela é necessária para detalhar RF-06 a RF-08. *Situação:* a aluna vai pedir ao orientador o contato ou a documentação técnica do responsável pelo TRANSCOLAR RURAL. Enquanto isso, os requisitos de integração seguem descritos de forma genérica (MQTT/API), sem fixar um formato de mensagem.
2. **Hardware e banco de dados definitivos** — continuam como decisões da Atividade 1.3 (10/2026). *Tendência registrada:* Raspberry Pi 5 + AI HAT (Hailo-10), já que o ESP32 não tem capacidade para rodar com folga os modelos pré-selecionados no benchmark (ArcFace/SFace) dentro do limite de 2 s do RNF-02. A escolha entre PostgreSQL e Firebase (RC-02) também fica para a 1.3. Os números de RNF-11 e RNF-12 serão fechados junto com essa decisão.

---

## 6. Rastreabilidade com os objetivos da proposta

| Objetivo específico (proposta) | Requisitos relacionados |
|---|---|
| Desenvolver protótipo de hardware IoT com câmera e microfone | RNF-11, RNF-12, RC-04 |
| Implementar algoritmos de reconhecimento facial e de voz | RF-01 a RF-05, RF-20, RNF-02, RNF-03, RNF-13, RNF-14 |
| Integrar o dispositivo ao TRANSCOLAR RURAL via rede móvel | RF-06, RF-07, RF-08, RC-03 |
| Criar relatórios inteligentes para gestores escolares | RF-09 a RF-15 |
| Avaliar desempenho, segurança e confiabilidade do sistema | RNF-01 a RNF-10, RNF-16, RF-21 |
