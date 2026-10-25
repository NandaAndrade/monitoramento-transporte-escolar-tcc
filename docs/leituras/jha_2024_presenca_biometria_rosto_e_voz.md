# Sistema de presença biométrico multimodal com fusão de rosto e fala no nível das características e detecção de vivacidade

> **Tradução integral para o português**, feita para estudo do TCC.
>
> **Original:** JHA, K.; JAIN, A.; SRIVASTAVA, S. Feature-level fusion of face and speech based multimodal biometric attendance system with liveness detection. *AIP Advances*, v. 14, 115007, 2024. DOI: [10.1063/5.0234430](https://doi.org/10.1063/5.0234430).
>
> **Licença:** o original é publicado em acesso aberto sob a licença [Creative Commons Atribuição 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br), © 2024 os autores. Esta tradução é uma obra derivada: o texto foi traduzido do inglês, as figuras foram substituídas por suas legendas e foram acrescentadas notas da tradução, marcadas como **[N. T.]**, e a seção final "Notas para o TCC". Os autores originais não revisaram nem endossam esta tradução.
>
> **PDF local:** `Downloads/Referencias/jha_2024_presenca_biometria_rosto_e_voz.pdf`

---

**Khushboo Jha, Aruna Jain e Sumit Srivastava**
Departamento de Ciência da Computação e Engenharia, Birla Institute of Technology, Ranchi, Índia.
Submetido em 21 ago. 2024; aceito em 22 out. 2024; publicado em 5 nov. 2024.

## Resumo

O rápido crescimento do aprendizado profundo e da Internet das Coisas estimulou a necessidade de sistemas biométricos sem contato em áreas onde a higiene e a interação não intrusiva com o usuário são críticas. Para autenticar de forma fluida, os métodos biométricos tradicionais, como o reconhecimento de impressão digital, de mão etc., exigem contato físico e, por isso, trazem riscos de higiene, o que torna a verificação de rosto e de locutor alternativas mais viáveis. Um Sistema de Presença Biométrico Multimodal (MBAS) robusto é necessário por causa das vulnerabilidades e limitações dos sistemas de modalidade única. Nesta pesquisa, apresentamos um MBAS que usa a fusão, no nível das características, de dados de fala com dados de rosto, combinando o melhor dos dois mundos. As características de textura baseadas na aparência facial da pessoa são integradas a informações dinâmicas da fala para a detecção de vivacidade, seguidas de redução de dimensionalidade por análise discriminante linear e, depois, incorporadas a um classificador Bi-LSTM. Assim, para melhor segurança, acurácia e proteção contra ataques de falsificação, esta abordagem é proposta para aumentar a acurácia e reforçar a segurança contra ataques de falsificação. Duas bases públicas, DeepfakeTIMIT e AVSpeech, são exploradas extensivamente para avaliar diferentes estratégias de fusão, tipos de classificador e métricas de desempenho padrão. O sistema proposto superou outros sistemas biométricos de ponta, com acurácia de 97,51%, precisão de 99,10% e taxa de erro igual de 2,48%. Esses resultados confirmam a eficácia e as possíveis aplicações reais do conceito de MBAS, junto com o reforço da segurança. Além disso, este estudo ressalta a importância de incorporar detecção de vivacidade avançada em soluções biométricas seguras e sem contato para a gestão moderna de presença em diversos setores, englobando as modalidades de rosto e de voz.

## I. Introdução

A importância crescente do aprendizado profundo e da tecnologia sem contato, impulsionada por preocupações de segurança e necessidades de saúde pública, expôs as limitações das biometrias convencionais, como a impressão digital¹ e o reconhecimento de íris². Esses dispositivos se mostraram eficazes em muitas aplicações, mas são invasivos e exigem contato físico, o que é menos desejável em ambientes compartilhados ou públicos, especialmente após pandemias globais como a de COVID-19. Além disso, os Sistemas Biométricos Unimodais (UBS)³, que usam apenas um atributo biológico, estão expostos a mudanças ambientais e a ataques de falsificação, o que os torna pouco confiáveis. Por exemplo, impressões digitais podem ser facilmente enganadas com digitais copiadas, e iluminação ruim ou óculos podem atrapalhar o reconhecimento de íris⁴. Esse contexto passou a exigir uma solução muito mais robusta, segura e higiênica: o Sistema Biométrico Multimodal (MBS)³, que combina várias características, em particular rosto e fala, para melhorar o desempenho e a confiabilidade.

Um Sistema de Presença Biométrico Multimodal (MBAS) não invasivo e sem contato, que usa reconhecimento de rosto e de fala (locutor), representa um grande avanço em autenticação. Ele combina esses dois métodos, aproveitando suas forças e compensando as fraquezas de depender apenas do reconhecimento facial ou apenas do de voz. O sistema se protege ainda mais contra falsificação ao incluir detecção de vivacidade baseada em textura (rosto) junto com detecção de vivacidade dinâmica, usando uma característica de fala sincronizada⁵, o que permite determinar se o dado biométrico capturado vem de uma pessoa viva ou de um objeto artificial. Consequentemente, essa dupla abordagem melhora não só a acurácia e a segurança, mas também a usabilidade em várias situações, sendo muito adequada para a gestão de presença em instituições de ensino, locais de trabalho e ambientes com Internet das Coisas (IoT), entre outros. Ela surge, portanto, como uma inovação muito pertinente no momento em que as organizações buscam soluções que unam segurança e conveniência para o usuário, como as soluções multimodais integradas.

Para manter alta acurácia na identificação de pessoas e, ao mesmo tempo, verificar a vivacidade⁶, o MBAS proposto usa técnicas avançadas de aprendizado profundo que extraem características de textura do rosto e características dinâmicas da fala, que depois são concatenadas no nível das características. Essa abordagem não só torna o sistema resistente à falsificação, como também tenta resolver os problemas de usar um único identificador biométrico, como as mudanças de aparência causadas por fatores ambientais. Além disso, combinar o classificador Bi-LSTM⁷ com um sistema de detecção de vivacidade⁶ resulta em um sistema de presença altamente seguro, eficiente e fácil de usar. Ele protege contra acessos não autorizados e mantém uma experiência fluida para o usuário, o que o torna ideal para a gestão moderna de presença em todos os setores.

## II. Trabalhos relacionados

O desenvolvimento de sistemas de autenticação biométrica seguros e eficientes⁸⁻⁹ recebeu bastante atenção nos últimos anos, sobretudo em aplicações que exigem interação sem contato⁶⁻⁸⁻¹¹. Cheniti *et al.*⁴ apresentaram um método sofisticado de autenticação de usuários com um sistema biométrico multimodal que integra dados de rosto e de impressão digital, com um arcabouço de fusão no nível das pontuações. Nessa abordagem, as pontuações geradas por cada modalidade biométrica são combinadas para melhorar a acurácia e a confiabilidade do sistema de autenticação. Técnicas de aprendizado profundo têm papel crucial na otimização¹²⁻¹³ do processo de fusão, permitindo ao sistema alcançar uma acurácia expressiva de 93,40% na base NIST-Set 2. Esse método destaca a importância de aproveitar várias características biométricas para melhorar o desempenho da autenticação, especialmente com classificadores de aprendizado profundo, capazes de captar padrões e dependências complexas nos dados. Na mesma linha, Rahman *et al.*¹⁴ aplicaram aprendizado profundo a outro sistema biométrico multimodal, combinando impressão digital e eletrocardiograma (ECG) no nível das características. Em vez de usar pontuações separadas de cada modalidade, as características extraídas da impressão digital e do ECG são fundidas em uma representação única, e uma CNN processa as características combinadas para a autenticação. Essa técnica aproveita o aprendizado profundo para extrair e aprender representações robustas das características, alcançando acurácia de 94,5%. O uso da CNN nesse contexto ressalta a eficácia do aprendizado profundo para captar os padrões intrincados dos dados biométricos multimodais. Vekariya *et al.*¹⁵ estenderam o uso do aprendizado profundo na autenticação multibiométrica, propondo uma técnica de fusão no nível das características que incorpora uma Máquina de Vetores de Suporte com Kernel Adaptativo Otimizada pelo Chimpanzé Binário (BCO-AKSVM) para seleção de características e classificação. Esse método usa aprendizado profundo para otimizar¹²⁻¹³ a escolha das características mais informativas e discriminativas de várias modalidades biométricas, garantindo que apenas as mais relevantes sejam usadas na autenticação. Os resultados experimentais dessa abordagem mostram alta acurácia, de 97%, evidenciando ainda mais o potencial de combinar aprendizado profundo e fusão no nível das características em sistemas biométricos. O uso do classificador BCO-AKSVM junto com a extração de características por aprendizado profundo melhora significativamente o processo de autenticação, tornando-o mais robusto e confiável. Em conjunto, esses estudos ressaltam o impacto crescente do aprendizado profundo nos sistemas biométricos multimodais. Ao permitir extração de características, fusão e classificação mais sofisticadas, o aprendizado profundo contribui para maior acurácia, mais segurança e maior resistência a ataques de falsificação na autenticação biométrica.

Os sistemas de presença biométricos tradicionais, como os de reconhecimento de impressão digital¹⁻¹⁶, mostraram limitações notáveis, especialmente em ambientes sensíveis à higiene, e vulnerabilidades como a suscetibilidade a ataques de falsificação⁶. Nos últimos anos, os sistemas de presença biométricos baseados em rosto e fala ganharam atenção como uma alternativa mais higiênica e segura. Vários pesquisadores propuseram soluções inovadoras de presença biométrica com técnicas avançadas de aprendizado profundo para melhorar a acurácia, a eficiência e a resistência a falsificações. Naufal *et al.*¹⁷ apresentaram um sistema de presença que combinou o método Haar Cascade com uma rede neural de aprendizado profundo para treinar as imagens faciais da base de dados. Esse método foi implementado em um sistema de câmera, permitindo reconhecimento facial rápido e eficiente para registro de presença. O sistema reconheceu rostos humanos com uma acurácia louvável de 95,23%, mostrando o potencial do aprendizado profundo para melhorar a acurácia de sistemas de presença biométricos. De forma semelhante, Wati *et al.*¹⁸ usaram o algoritmo de Viola-Jones para detectar rostos, seguido de extração de características com wavelets de Gabor e casamento de modelos (*template matching*) para a classificação. No entanto, o sistema alcançou uma acurácia menor, de 75%, indicando que melhorias na extração de características e nos modelos de classificação poderiam elevar o desempenho.

Ismail *et al.*¹⁹ desenvolveram um sistema de presença por reconhecimento facial baseado na web, que usou modelos de aprendizado profundo pré-treinados de código aberto, especificamente a ResNet34, combinada com a distância euclidiana para a classificação. O sistema teve alto desempenho de reconhecimento facial, com acurácia de 92%, precisão de 100% e *recall* de cerca de 90%. Esse trabalho mostrou a eficácia de integrar modelos de aprendizado profundo pré-treinados a sistemas biométricos, com bom equilíbrio entre acurácia e eficiência computacional. Porém, ele não incorporou detecção de vivacidade, deixando o sistema vulnerável a falsificações. Para atender à necessidade de detecção de vivacidade, Surantha e Sugijakko⁵ propuseram um sistema de presença leve com detecção de vivacidade usando o modelo MobileNetV2 e aprendizado por transferência. A abordagem se concentrou em diferenciar pessoas vivas de ataques de falsificação, alcançando acurácia de 96% para pessoas vivas e de cerca de 79% na detecção de ataques de falsificação de nível A. O tempo médio de processamento foi inferior a 0,6 s, o que a torna uma solução eficiente para sistemas de presença em tempo real. Esse estudo destacou a importância da detecção de vivacidade em sistemas biométricos, sobretudo para evitar ataques de falsificação.

Além disso, Becerra *et al.*¹⁶ exploraram sistemas de presença baseados em fala, com extração de coeficientes cepstrais na escala Mel (MFCC) e um classificador CNN. O sistema alcançou acurácia de 97%, mostrando o potencial da biometria por fala em sistemas de presença sem contato. No entanto, essa abordagem, como muitas outras, não incorporou detecção de vivacidade, ficando suscetível a falsificações. Entre essas abordagens, apenas Surantha e Sugijakko⁵ incorporaram detecção de vivacidade ao sistema de presença, o que reforça a necessidade de integrá-la para se defender de ataques de falsificação⁶. A detecção de vivacidade é crucial para diferenciar amostras biométricas genuínas de amostras falsas ou forjadas, garantindo a segurança dos sistemas biométricos. Apesar desses avanços, ainda há uma lacuna significativa no desenvolvimento de sistemas de presença biométricos multimodais que incorporem detecção de vivacidade para aumentar a segurança e a aceitação pelos usuários. São necessárias mais pesquisas sobre sistemas de presença biométricos multimodais sem contato com técnicas robustas de detecção de vivacidade, para atender às demandas da era digital e garantir alta acurácia, segurança e boa experiência do usuário.

## III. Formulação do problema

Os Sistemas de Presença Biométricos Unimodais (UBAS)¹⁷⁻²⁰, embora amplamente adotados pela conveniência, costumam ser vulneráveis a desafios como falsificação, variabilidade ambiental e falhas de ponto único. Por exemplo, o reconhecimento facial⁹ pode ser enganado por imagens ou vídeos de alta qualidade, e o reconhecimento de fala/locutor⁸ pode ser comprometido por áudio pré-gravado. Para tratar essas vulnerabilidades, este artigo propõe um novo MBAS que integra o reconhecimento de rosto e de fala (locutor) no nível das características, com detecção de vivacidade avançada baseada em características de textura (rosto) e dinâmicas (fala), reforçando a segurança e a confiabilidade. Assim, usando extração de características por aprendizado profundo e um classificador Bi-LSTM⁷⁻²⁰, o sistema proposto distingue de forma eficaz entradas genuínas de falsificadas, o que o torna particularmente adequado para aplicações sensíveis, como o registro de presença com IoT⁵⁻²¹. A metodologia é avaliada rigorosamente em comparação com abordagens tradicionais e métricas de desempenho, mostrando acurácia e robustez superiores.

## IV. Metodologia proposta

No MBAS proposto, duas fases distintas, treinamento e teste⁸, são componentes essenciais. Na fase de treinamento, os usuários iniciam o processo fazendo seu cadastro. Isso envolve capturar um vídeo curto com uma câmera com sensor inteligente, do qual o sinal de fala é pré-processado para extrair atributos dinâmicos confiáveis da fala. Ao mesmo tempo, o quadro com a imagem facial é extraído do vídeo para permitir uma extração eficaz de características de textura. Os vetores de características resultantes das duas modalidades são enviados à detecção de vivacidade⁶. Se o valor da detecção de vivacidade estiver abaixo do limiar, o pedido de autenticação é rejeitado; caso contrário, os vetores são concatenados para obter a fusão no nível das características, com o objetivo de aproveitar as informações complementares fornecidas pelos sinais de áudio e visuais. Em seguida, um classificador é usado para treinar esses modelos fundidos (*templates*), como mostra a Figura 1. Os modelos treinados são então armazenados em um banco de dados para as fases de teste seguintes.

Na fase de teste⁸, que espelha o processo de treinamento, verifica-se a autenticidade da identidade alegada pelo usuário. O usuário apresenta seu modelo biométrico fundido, que é comparado com os modelos de referência treinados armazenados no banco de dados. Essa comparação é feita de forma um-para-um, em que o modelo do usuário alegado é examinado em relação a todos os modelos cadastrados para verificar sua legitimidade. **[N. T.: o texto diz "um-para-um", mas descreve uma comparação com todos os cadastrados, o que seria um-para-muitos.]** A decisão final sobre a autenticidade do usuário é tomada com base no grau de semelhança entre o modelo consultado e os dados de referência, medido por métricas de desempenho predefinidas. Essa abordagem garante uma avaliação abrangente da identidade alegada, aproveitando várias modalidades biométricas. Ao integrar as características faciais e de fala no nível das características, o sistema busca aumentar a acurácia da autenticação e a resistência a tentativas de falsificação. Além disso, as fases sistemáticas de treinamento e teste fornecem um arcabouço robusto para a autenticação de usuários⁴⁻¹¹, fortalecendo a segurança do MBAS.

> [Figura 1: Sistema de presença biométrico multimodal.]

### A. Pré-processamento

No campo do processamento de imagens para reconhecimento facial⁹⁻²², técnicas de pré-processamento de ponta¹⁻⁶⁻²³ precedem a extração de características e geralmente envolvem várias etapas para melhorar a qualidade e a informatividade das imagens. Neste trabalho, técnicas como redução de ruído, realce de contraste e normalização¹⁻⁶⁻²³ são aplicadas para garantir consistência entre imagens diferentes. Além disso, técnicas de aumento de dados¹⁷⁻²⁰⁻²⁴, como espelhamento, rotação e mudança de escala, são usadas para aumentar artificialmente a diversidade da base, melhorando a robustez e a capacidade de generalização do modelo. Essas etapas de pré-processamento²³ buscam atenuar variações de iluminação, de ponto de vista e de outros fatores ambientais, facilitando uma extração de características mais precisa e a análise seguinte. De forma semelhante, no pré-processamento da fala²³, uma técnica de redução de ruído de ponta²⁵⁻²⁶, implementada com recursos nativos da linguagem Python, é aplicada antes da extração de características para melhorar a qualidade e o poder discriminativo das amostras de fala. Ela inclui redução de ruído para melhorar a relação sinal-ruído, filtragem para remover frequências irrelevantes e normalização para padronizar os níveis de amplitude. Essas etapas de pré-processamento têm papel crucial na preparação das amostras de fala para as análises seguintes, como o reconhecimento de locutor⁸⁻²⁵.

### B. Extração de características

#### 1. Rosto

No contexto da detecção de vivacidade facial e da extração de características²⁷, inspirados no nosso trabalho anterior apresentado na Ref. 6, escolhemos uma abordagem baseada em textura que integra wavelets de Gabor (GW)⁶ e padrões binários locais (LBP)⁶⁻⁹, chamada GW-LBP, como mostra a Figura 2. Neste trabalho, os filtros de Gabor são aplicados para extrair características de textura em 5 escalas e 8 orientações⁶, com vetor de características de comprimento total 5 × 8 = 40. Para a extração do LBP, com raio 1 e 8 vizinhos, o vetor de características tem comprimento total de 2⁸ = 256. Assim, o vetor combinado tem comprimento 40 + 256 = 296, isto é, a fusão GW-LBP capta a informação de textura global (GW) e local (LBP)⁶. Além disso, ao aproveitar as forças dos dois métodos, obtém-se um conjunto de características mais completo, o que melhora a discriminação entre rostos vivos⁶ e falsos, e também o sistema de reconhecimento.

> [Figura 2: Característica facial: wavelet de Gabor e padrão binário local.]

#### 2. Fala

No contexto da detecção de vivacidade na fala e da extração de características²³, as características dinâmicas são consideradas o estado da arte, por focarem nas variações de altura (*pitch*), entonação e ritmo²³, difíceis de reproduzir em uma gravação falsificada. Por isso, neste trabalho, escolhemos os coeficientes cepstrais de Q constante (CQCC)²⁸ e as características de formantes⁸, chamados em conjunto de CQCC-F. Os CQCC²⁸ representam a resolução espectro-temporal, que registra com precisão os artefatos de adulteração. Os artefatos de adulteração denotam a característica dos ataques de falsificação, o que aumenta a acurácia do sistema. Além disso, as frequências dos formantes derivam das propriedades físicas do trato vocal, e reproduzi-las com precisão em uma gravação falsificada é difícil. Por exemplo, a variação natural das frequências dos formantes durante a fala ao vivo (por causa dos movimentos articulatórios) costuma estar ausente ou ser mal reproduzida em ataques de reprodução de gravação. A característica CQCC-F ajuda a detectar artefatos que podem estar presentes em gravações falsificadas, mas não na fala ao vivo, como pausas não naturais, falta de modulação natural da frequência ou distorções na estrutura dos formantes. Assim, ela oferece uma análise abrangente tanto do conteúdo espectral (pelos CQCC) quanto das características fisiológicas (pelos formantes) do sinal de fala, o que é crucial para o reconhecimento de locutor²³ e a detecção de vivacidade. A técnica de extração dos CQCC²⁸ envolve o espectro de potência em escala logarítmica e a análise cepstral dos sinais de fala. O espectro de potência logarítmico calcula o espectro de potência dos coeficientes da Transformada de Q Constante (CQT)²⁸ e aplica um logaritmo para comprimir a faixa dinâmica, como na equação:

$$P_{CQ}(k, t) = \log\left(\lvert X_{CQ}(k, t)\rvert^2\right) \tag{1}$$

em que $X_{CQ}(k, t)$ é o coeficiente da CQT na faixa de frequência $k$. Para a análise cepstral, aplicamos a Transformada Discreta de Cosseno (DCT)²⁸ ao espectro de potência logarítmico para obter os CQCC, como na equação:

$$c_m = \sum_{k=1}^{K} P_{CQ}(k, t) \cos\left[\frac{\pi m}{K}\left(k - \frac{1}{2}\right)\right] \tag{2}$$

em que $c_m$ é o coeficiente CQCC, $m$ é o índice do coeficiente cepstral e $K$ é o número total de faixas de frequência. Aqui, extraímos 19 características CQCC. Além disso, para as características de formantes, usamos a análise de Codificação Preditiva Linear (LPC), que modela o sinal de fala como uma combinação linear de suas amostras passadas, como na equação:

$$s[n] = \sum_{p=1}^{P} a_p\, s[n - p] + e[n] \tag{3}$$

em que $s[n]$ é a amostra atual, os $a_p$ são os coeficientes LPC, $P$ é a ordem da predição e $e[n]$ é o erro residual. Aqui, extraímos as três primeiras frequências de formantes, F1, F2 e F3⁸, a partir dos coeficientes LPC²⁵, usando algoritmos de busca de raízes. Assim, um total de 22 características de fala é usado para a detecção de vivacidade e para o reconhecimento de locutor.

### C. Redução de dimensionalidade das características

A redução de dimensionalidade²⁹ é crucial em MBS, especialmente diante de dados de alta dimensão vindos de fontes mistas, como imagens faciais e sinais de fala, mantendo a separabilidade entre as classes. Nesse sentido, integrar as características das duas modalidades resulta em um espaço de características grande, o que aumenta a complexidade computacional, o risco de sobreajuste e a redundância de características irrelevantes. Para garantir que apenas as características mais discriminativas permaneçam e que o restante do espaço seja reduzido, preservando a informação relevante de separabilidade entre classes para evitar o sobreajuste, foi usada a Análise Discriminante Linear (LDA)²⁹. A LDA minimiza a dispersão intraclasse $S_w$ e maximiza a dispersão interclasse $S_b$ para aumentar a separabilidade das classes. A LDA encontra a matriz de projeção $W$²⁹ que maximiza a razão entre a dispersão interclasse e a intraclasse, como na equação:

$$W = \arg\max \frac{\lvert W^T S_b W\rvert}{\lvert W^T S_w W\rvert} \tag{4}$$

Em seguida, o vetor combinado de características de rosto e fala, $F_{FFS}$, é mapeado para um espaço de dimensão menor, representado pela equação:

$$X_{LDA} = W^T F_{FFS} \tag{5}$$

Ao aplicar a LDA²⁹, o sistema reduz a dimensionalidade dos vetores concatenados de características faciais e de fala, preservando a informação discriminativa necessária para uma classificação precisa. Além disso, ela melhora o desempenho do classificador Bi-LSTM⁷⁻³⁰, permitindo cálculos mais rápidos, melhor acurácia e generalização robusta em cenários reais. Consequentemente, a redução de dimensionalidade por LDA é uma ferramenta importante para projetar MBAS eficientes e escaláveis.

### D. Fusão das características de rosto e fala

A fusão no nível das características⁴⁻³¹⁻³² oferece vantagens claras sobre outros tipos de fusão para integrar características de fala e de imagem. Ao contrário da fusão no nível da decisão, que combina as saídas de classificadores separados, e da fusão no nível do sensor³², que junta os dados brutos de vários sensores, a fusão no nível das características opera diretamente sobre as características extraídas de cada modalidade. Essa abordagem preserva o conteúdo de informação original e permite uma integração mais refinada, com vários benefícios principais. Primeiro, a fusão no nível das características¹⁴ capta melhor a natureza complementar das modalidades de fala e imagem, combinando diretamente as características extraídas. Isso permite uma representação mais rica dos dados, aumentando a capacidade do sistema de captar relações complexas entre as modalidades. Segundo, ela normaliza o espaço de características fundido, em comparação com a fusão no nível da decisão, o que pode melhorar a eficiência computacional e reduzir a complexidade das etapas de processamento seguintes. Além disso, facilita a integração de conjuntos de características diversos, permitindo incorporar conhecimento específico do domínio e garantindo flexibilidade no projeto do modelo. No geral, neste trabalho, a fusão no nível das características oferece uma abordagem mais holística, pelo método de concatenação, para integrar características de fala e de imagem, resultando em melhor desempenho do sistema, maior poder discriminativo e mais flexibilidade em aplicações multimodais, como biometria, interação humano-computador e análise multimídia.

### E. Classificador

A Bi-LSTM³³ é um tipo de rede neural recorrente (RNN)³⁴, o que a torna muito eficaz para analisar características temporais, como mudanças na textura facial e padrões dinâmicos de fala, já que capta dependências tanto para frente quanto para trás em dados sequenciais. Esse processamento bidirecional se torna importante quando é preciso captar pistas muito sutis que diferenciam pessoas vivas de ataques de falsificação. Por isso, o classificador Bi-LSTM de ponta⁷⁻³³ mostrado na Tabela I é usado neste estudo, por ser superior a outros classificadores em MBS. Uma vantagem que diferencia a Bi-LSTM de outros modelos³⁰ é a capacidade de captar dependências de longo prazo e a dinâmica temporal dos dados de entrada. Ao contrário de classificadores tradicionais, como máquinas de vetores de suporte (SVM)³⁵ ou florestas aleatórias (RF)³⁶, a Bi-LSTM capta informações de contexto em horizontes de tempo longos, o que pode ser essencial para modelar melhor padrões sequenciais. Isso a torna mais confiável para relações complexas entre características de fala e de rosto, melhorando o desempenho em verificação de locutor, detecção de vivacidade, fusão multimodal e outras tarefas. Além disso, a arquitetura bidirecional da Bi-LSTM permite processar as sequências de entrada nos dois sentidos, captando informação de contexto dos passos de tempo passados e futuros. Esse processamento bidirecional aumenta a capacidade do modelo de captar dependências temporais e melhora sua robustez a variações nos dados de entrada. Neste trabalho, o modelo Bi-LSTM⁷ é composto por uma camada de entrada, duas camadas LSTM, duas camadas de *dropout* e uma camada de saída. Dados sequenciais, como as características fundidas de fala e rosto em forma de série temporal, entram pela camada de entrada, que os passa às camadas de processamento seguintes.

**Tabela I.** Descrição do classificador Bi-LSTM.

| Camada | Configuração |
|---|---|
| Camada de entrada | — |
| Camada LSTM | 128 unidades; função de ativação ReLU; *dropout* = 0,5 |
| Camada LSTM | 128 unidades; função de ativação ReLU; *dropout* = 0,2 |
| Camada de saída | Otimizador SGD (gradiente descendente estocástico); função de ativação sigmoide |

Em seguida, entram em ação as células de memória das camadas LSTM⁷, que armazenam informações por longos períodos e permitem ao modelo aprender padrões temporais complexos. A arquitetura usada neste estudo tem duas camadas LSTM, cada uma com o número de unidades (neurônios) que o usuário desejar. Para evitar o sobreajuste e melhorar a generalização, camadas de *dropout* são incluídas entre as camadas LSTM. O *dropout* desativa aleatoriamente uma parte dos neurônios durante o treinamento, forçando o modelo a aprender representações mais robustas dos dados.

Por fim, depois de várias iterações, cada uma ajustando os pesos até que não seja mais necessário ajustá-los, a camada de saída recebe os dados processados das camadas LSTM e dá a classificação ou predição final. Dependendo da função que o sistema deve executar, por exemplo SoftMax para classificação e ativação linear para regressão, escolhe-se a função de ativação da camada de saída. **[N. T.: a Tabela I indica ativação sigmoide na saída.]** De modo geral, o classificador Bi-LSTM proposto supera os existentes ao explorar a dinâmica temporal das características de fala e de textura facial no MBAS, resultando em autenticação mais precisa e robusta.

## V. Resultados e discussão

O MBAS proposto foi implementado na linguagem Python. O treinamento (80%) e o teste (20%) do modelo foram feitos combinando duas bases públicas padrão de vídeo, DeepfakeTIMIT³⁷ e AVSpeech³⁸. A base DeepfakeTIMIT contém duas categorias de vídeos *deepfake* gerados por GAN: baixa qualidade (entrada de 64 × 64) e alta qualidade (entrada de 128 × 128). Os vídeos originais de 32 pessoas da VidTIMIT⁸ foram selecionados e divididos em 16 pares, resultando em 10 vídeos de troca de rosto por par. Isso dá um total de 320 vídeos de cada qualidade e 640 vídeos ao todo. A AVSpeech³⁸ é uma grande coleção audiovisual de vídeos de fala. Cada trecho, de três a dez segundos, mostra um locutor visível no vídeo. Cerca de 4.700 h de trechos de vídeo, vindos de 290 mil vídeos do YouTube, cobrem um amplo espectro de pessoas, idiomas e expressões faciais. Para este estudo, foi selecionado um subconjunto de 1.280 vídeos, 640 de cada base. A duração média dos vídeos é de 4,25 s, com 106 quadros por gravação. O áudio correspondente é armazenado como arquivo WAV mono de 16 bits e 32 kHz⁸. A integração dessas bases é particularmente valiosa para melhorar a detecção de vivacidade e a resistência à falsificação do MBAS. Ao usar uma mistura de dados autênticos e de *deepfakes* gerados por GAN, o sistema é testado rigorosamente contra técnicas de falsificação, tornando-se mais robusto para detectar características biométricas genuínas e resistir a possíveis ataques.

### A. Análise do MBAS proposto em comparação com o UBAS

Esta análise comparativa avalia a eficácia de um sistema de presença que usa o reconhecimento de fala e o de rosto como Sistemas de Autenticação Biométrica Unimodais (UBAS), especificamente o reconhecimento de locutor⁸ e o reconhecimento facial⁹⁻¹⁷, em comparação com o MBAS proposto, que integra as duas modalidades na autenticação dos usuários¹¹. A avaliação da Tabela II se concentra nas medidas de acurácia⁶ e de taxa de erro igual (EER)⁶ para avaliar a eficácia dos sistemas. A robustez e a confiabilidade do sistema são esclarecidas pela análise da acurácia de cada modalidade biométrica isolada e da sua integração no MBAS. Além disso, a Figura 3 apresenta a análise da curva ROC⁶ para os UBAS de rosto e de fala e para o MBAS.

**Tabela II.** Avaliação do MBAS proposto em comparação com o UBAS.

| Sistema biométrico | Características usadas | Acurácia (%) | EER (%) |
|---|---|---|---|
| UBAS com fala | CQCC-F | 94,76 | 7,14 |
| UBAS com rosto | GW-LBP | 96,23 | 5,29 |
| MBAS (proposto) | Fusão no nível das características de CQCC-F e GW-LBP | 97,51 | 2,48 |

A curva ROC avalia de forma mais eficaz o desempenho de um sistema de classificação binária (real ou falsificado). Ela traça a taxa de verdadeiros positivos em função da taxa de falsos positivos (FPR), dando uma visão dos dois tipos de erro e permitindo comparar sistemas diferentes com facilidade. Além disso, é uma estatística essencial em problemas de classificação por gerar uma avaliação independente do limiar, mostrar graficamente as compensações e lidar com bases desbalanceadas. O sistema com a maior área sob a curva ROC, aqui o MBAS, é considerado superior aos demais. Além disso, pela Tabela II, a EER dá uma avaliação completa da capacidade do sistema de manter equilibradas as taxas de falsa aceitação e de falsa rejeição⁶. As técnicas de detecção de vivacidade reduzem a EER de forma eficaz, tornando o sistema altamente resistente a ataques de falsificação. Essa análise comparativa esclarece as vantagens e desvantagens dos sistemas unimodais em relação ao MBAS em termos de desempenho, o que pode abrir caminho para melhores soluções de autenticação no mundo real.

> [Figura 3: Desempenho da curva ROC para os diferentes sistemas.]

### B. Análise do sistema proposto com vários níveis de fusão das características de fala e rosto

A avaliação da metodologia proposta inclui vários tipos de fusão dos atributos de rosto e fala: por posição (*rank*), por pontuação, por decisão, por sensor e por características. Avaliamos o desempenho e a eficácia de cada nível de fusão na melhoria da acurácia da autenticação, da resistência a ataques de falsificação e da experiência do usuário, por meio de análise e experimentação cuidadosas. Os resultados dos vários procedimentos de fusão, apresentados na Tabela III, são avaliados com várias medidas convencionais baseadas na matriz de confusão⁶⁻¹⁰⁻³⁹.

O objetivo desta pesquisa é determinar as melhores configurações para aumentar a segurança e a usabilidade, garantindo ao mesmo tempo a conformidade com as normas regulatórias. Esse exame minucioso dá uma compreensão significativa das vantagens e desvantagens de cada nível de fusão, orientando os próximos avanços em segurança. Para facilitar a compreensão dos dados da Tabela III, foi incluída uma análise comparativa na Figura 4. Essa figura ilustra a eficácia da metodologia proposta (em %) nos diferentes níveis de fusão: decisão, pontuação, posição, sensor e características.

**Tabela III.** Análise do MBAS proposto (em %) com vários níveis de fusão.

| Métrica | Pontuação | Decisão | Sensor | Posição | Características (proposta) |
|---|---|---|---|---|---|
| Acurácia | 94,90 | 91,07 | 88,14 | 89,42 | 97,51 |
| Sensibilidade | 96,26 | 92,27 | 87,29 | 86,44 | 99,02 |
| Especificidade | 92,38 | 88,18 | 80,85 | 86,58 | 96,00 |
| Precisão | 95,14 | 94,99 | 89,41 | 86,70 | 99,10 |
| Medida F | 96,33 | 93,61 | 88,34 | 86,57 | 98,33 |
| MCC | 88,56 | 86,53 | 87,50 | 80,71 | 97,90 |
| NPV | 90,98 | 88,62 | 87,45 | 84,16 | 94,50 |
| FPR | 11,81 | 10,50 | 16,64 | 14,14 | 4,01 |
| FNR | 7,73 | 9,37 | 8,70 | 9,78 | 0,96 |
| EER | 9,77 | 9,93 | 12,67 | 11,96 | 2,48 |

> [Figura 4: Comparação gráfica do MBAS proposto (em %) com vários níveis de fusão de dados.]

**[N. T.: em várias colunas das Tabelas III e IV, FPR + especificidade não soma 100%, como deveria (por exemplo, 96,00 + 4,01 na coluna proposta). Os valores foram mantidos como no original.]**

### C. Análise da abordagem proposta com diferentes classificadores

O exame do método proposto inclui avaliar diferentes classificadores para determinar sua eficácia no arcabouço do MBAS proposto. Por meio de experimentação e análise comparativa cuidadosas¹⁰⁻³⁹, examinamos a eficácia de vários classificadores, como o modelo de mistura de gaussianas (GMM)³⁵, a SVM³⁵, a RF³⁶, a CNN⁸⁻⁹⁻⁴⁰ e as redes Bi-LSTM³³, como detalha a Tabela IV. Pela análise de métricas como acurácia⁴⁰, EER e vários aspectos de eficiência computacional, o objetivo é determinar o classificador que oferece a melhor combinação de desempenho, robustez e escalabilidade para o sistema proposto. Além disso, este exame explora a capacidade do classificador de lidar com as complexidades da fusão de dados multimodais, incluindo a integração no nível das características de atributos auditivos e visuais, e sua robustez contra tentativas de falsificação. Essa avaliação minuciosa busca trazer informações importantes sobre a eficácia de vários classificadores para melhorar a segurança e reduzir ameaças cibernéticas. Os resultados aprimoram significativamente os sistemas de autenticação biométrica voltados à proteção de infraestruturas críticas em contextos de autenticação digital. Para facilitar a compreensão dos dados da Tabela IV, foi incluída uma análise comparativa na Figura 5. Essa figura ilustra a eficácia da metodologia proposta (em %) com MBAS baseados em diferentes classificadores.

**Tabela IV.** Avaliação do MBAS proposto (em %) com diferentes classificadores.

| Métrica | GMM | SVM | RF | CNN | Bi-LSTM (proposto) |
|---|---|---|---|---|---|
| Acurácia | 91,09 | 90,07 | 92,14 | 95,42 | 97,51 |
| Sensibilidade | 90,26 | 89,27 | 91,29 | 95,44 | 99,02 |
| Especificidade | 89,38 | 87,18 | 84,85 | 85,58 | 96,00 |
| Precisão | 89,18 | 93,99 | 93,41 | 92,70 | 99,10 |
| Medida F | 88,99 | 92,61 | 92,34 | 92,57 | 98,33 |
| MCC | 87,56 | 85,53 | 91,50 | 86,71 | 97,90 |
| NPV | 88,23 | 82,62 | 88,45 | 85,16 | 95,50 |
| FPR | 11,61 | 10,37 | 14,14 | 8,64 | 4,01 |
| FNR | 8,73 | 9,50 | 6,70 | 3,78 | 0,96 |
| EER | 10,17 | 9,94 | 10,42 | 6,21 | 2,48 |

**[N. T.: a NPV do Bi-LSTM é 95,50 na Tabela IV e 94,50 na Tabela III, para o mesmo sistema.]**

> [Figura 5: Comparação gráfica do MBAS proposto (em %) com MBAS baseados em vários classificadores.]

### D. Comparação com alguns MBS de ponta

Este estudo mostra avanços inovadores na área de MBS e de sua aplicação, em particular ao explorar o uso combinado do reconhecimento facial e da análise de áudio para autenticar usuários. A literatura atual se concentra principalmente na combinação de expressões faciais com modalidades que não a fala, ou vice-versa, como mostra a Tabela V. Rahman *et al.*¹⁴ apresentaram uma técnica de fusão de impressão digital e ECG no nível das características, usando uma CNN como classificador. Com base nos resultados dos experimentos, a abordagem alcança acurácia de 94,5%. Vekariya *et al.*¹⁵ propuseram uma técnica de autenticação multibiométrica que também envolve fusão no nível das características. O método usa uma Máquina de Vetores de Suporte com Kernel Adaptativo Otimizada pelo Chimpanzé Binário (BCO-AKSVM) para determinar as características mais eficazes. Os resultados experimentais do método mostram alta acurácia, de 97%.

**Tabela V.** Comparação de desempenho da abordagem proposta com MBS de ponta, em termos de acurácia.

| Referência e ano | Característica biométrica | Tipo de fusão | Acurácia (%) |
|---|---|---|---|
| Alagarsamy *et al.*, 2022 | Rosto e orelha | Pontuação | 96,24 |
| Rahman *et al.*, 2024 | ECG e impressão digital | Características | 94,50 |
| Varaiya *et al.*, 2024 | Rosto e impressão digital | Características | 97,00 |
| Cheniti *et al.*, 2024 | Rosto e impressão digital | Pontuação | 93,40 |
| Proposto | Rosto e fala | Características | 97,51 |

**[N. T.: nas Tabelas V e VI, os números de referência do original não correspondem à lista de referências (por exemplo, Rahman é a ref. 14 no texto e aparece como 23 na tabela), por isso foram omitidos. "Varaiya" parece ser Vekariya, ref. 15; e o texto da Seção II diz que Vekariya fundiu "várias modalidades", sem citar rosto e impressão digital.]**

**Tabela VI.** Comparação de desempenho do MBAS proposto com sistemas de presença biométricos de ponta.

| Referência e ano | Característica biométrica | Detecção de vivacidade | Método | Acurácia (%) |
|---|---|---|---|---|
| Naufal *et al.*, 2021 | Rosto | Não | Haar cascade com CNN | 95,23 |
| Wati *et al.*, 2021 | Rosto | Não | Wavelet de Gabor com busca *best first* | 75 |
| Ismail *et al.*, 2022 | Rosto | Não | ResNet-34 com distância euclidiana | 92 |
| Surantha *et al.*, 2024 | Rosto | Sim | MobileFaceNet com CNN | 96 |
| Becerra *et al.*, 2024 | Fala | Não | MFCC com CNN | 97 |
| Proposto | Rosto e fala | Sim | CQCC-F e GW-LBP com Bi-LSTM | 97,51 |

**[N. T.: a Seção II descreve o trabalho de Surantha e Sugijakko com MobileNetV2, e a Tabela VI com MobileFaceNet.]**

A Tabela V destaca a eficácia do MBAS proposto em aumentar a acurácia e a robustez em comparação com outros MBS de ponta. Para dar uma visão mais aprofundada, a Tabela VI apresenta uma comparação de desempenho do MBAS proposto com alguns sistemas de presença biométricos de ponta que usam metodologias semelhantes. Essa comparação⁵⁻¹⁶⁻¹⁹ se concentra em fatores críticos, incluindo as características biométricas usadas, a integração de técnicas de detecção de vivacidade, os métodos de extração de características e de classificação empregados e a acurácia geral alcançada. De acordo com os resultados⁵⁻¹⁶⁻¹⁹, em comparação com o MBAS, a maioria dos sistemas de ponta se baseava em uma única biometria para registro de presença, com uma rede neural convolucional (CNN) como classificador. Ao analisar alguns parâmetros, o estudo comparativo ressalta as vantagens do sistema biométrico multimodal proposto em termos de detecção de vivacidade aprimorada, uso de técnicas avançadas de aprendizado profundo e acurácia superior em vários cenários. Os resultados mostram que integrar características faciais de textura e características dinâmicas de fala para uma detecção de vivacidade robusta, com um classificador Bi-LSTM, melhora significativamente o desempenho geral do MBAS.

Além disso, podemos inferir que o vetor de características baseado em LDA, junto com a capacidade da Bi-LSTM de captar dependências para frente e para trás em dados sequenciais, torna o sistema altamente eficaz na análise de características temporais, como variações na textura facial e padrões dinâmicos de fala. Esse processamento bidirecional é crucial para detectar pistas sutis de vivacidade, como movimentos faciais naturais ou modulações autênticas da voz, difíceis de reproduzir em ataques de falsificação. Os resultados mostram claramente que incorporar a técnica LDA, a fusão no nível das características de vetores normalizados e a Bi-LSTM melhora a acurácia e a robustez do MBAS, levando a um melhor desempenho geral do sistema. Essa vantagem é particularmente evidente em cenários com tentativas complexas de falsificação, em que os classificadores tradicionais podem ter dificuldade, o que reforça a importância do MBAS para alcançar acurácia de reconhecimento superior e resistência confiável à falsificação.

## VI. Conclusão

Esta pesquisa propõe uma abordagem inovadora e sem contato para um sistema de presença seguro e confiável, usando um sistema biométrico multimodal (MBS) que integra características faciais e de fala por meio de fusão no nível das características. Ao combinar as características de rosto e de fala, o sistema aproveita as forças complementares de cada modalidade, compensando de forma eficaz as limitações de depender de uma única característica biométrica. Uma novidade importante está na incorporação de dois mecanismos de detecção de vivacidade: detecção baseada em textura para o rosto e detecção dinâmica sincronizada com as características da fala. Essa combinação permite ao sistema verificar se os dados biométricos vêm de uma pessoa viva ou de uma fonte artificial, aumentando significativamente a segurança contra tentativas de falsificação. Além disso, o estudo incorpora técnicas de redução de dimensionalidade, como a LDA, para aumentar a separabilidade das classes, seguidas de fusão no nível das características e classificação com um classificador Bi-LSTM. O classificador Bi-LSTM, conhecido por captar dependências de longo prazo e dinâmicas temporais, aumenta a robustez e a adaptabilidade em cenários de autenticação de presença em tempo real. Essa abordagem trata desafios importantes, como melhorar a acurácia da autenticação, reduzir a vulnerabilidade a falsificações e garantir a conformidade com a privacidade, oferecendo ao mesmo tempo uma experiência fluida ao usuário. O método proposto foi testado rigorosamente na combinação das bases DeepfakeTIMIT e AVSpeech, alcançando desempenho excepcional, com acurácia de 97,51%, precisão de 99,10% e EER de 2,48%, superando soluções de ponta. Esses resultados mostram a eficácia do sistema em contextos reais, evidenciando seu potencial para prevenir ameaças de segurança e proteger infraestruturas críticas. O MBS proposto serve como modelo pioneiro para sistemas de presença biométricos mais fortes e resilientes, avançando o desenvolvimento de arcabouços de autenticação seguros na era digital.

## Declarações dos autores

**Conflito de interesses:** os autores não têm conflitos a declarar.

**Contribuições dos autores:** Khushboo Jha: concepção (igual); investigação (igual); validação (igual); redação do rascunho original (igual). Aruna Jain: administração do projeto (igual); redação, revisão e edição (igual). Sumit Srivastava: administração do projeto (igual); redação, revisão e edição (igual).

**Disponibilidade dos dados:** os dados que sustentam os resultados deste estudo estão disponíveis com o autor correspondente mediante solicitação razoável.

## Referências

As referências estão no idioma original.

1. H. Mohamed, Y. Liu, K. Wang, "Multimodal biometric authentication systems using convolution neural network based on different level fusion of ECG and fingerprint," IEEE Access 7, 26527–26542 (2018).
2. J. E. Zambrano, J. I. Pilataxi, C. A. Perez, K. W. Bowyer, "Iris recognition using an enhanced pre-trained backbone based on anti-aliased CNNs," IEEE Access 12, 94570 (2024).
3. M. O. Oloyede, G. P. Hancke, "Unimodal and multimodal biometric sensing systems: A review," IEEE Access 4, 7532–7555 (2016).
4. M. Cheniti, Z. Akhtar, C. Adak, K. Siddique, "An approach for full reinforcement-based biometric score fusion," IEEE Access 12, 49779 (2024).
5. N. Surantha, B. Sugijakko, "Lightweight face recognition-based portable attendance system with liveness detection," Internet Things 25, 101089 (2024).
6. K. Jha, S. Srivastava, A. Jain, "A novel texture based approach for facial liveness detection and authentication using deep learning classifier," Int. J. Comput. Exp. Sci. Eng. 10(3), 323–331 (2024).
7. V. Rai, G. Gupta, S. Joshi, R. Kumar, A. Dwivedi, "LSTM-based adaptive whale optimization model for classification of fused multimodality medical image," Signal Image Video Process. 17, 2241 (2023).
8. K. Jha, A. Jain, S. Srivastava, "An efficient speaker identification approach for biometric access control system," IEEE 5th International Conference on Recent Advances in Information Technology (RAIT), 2023, pp. 1–5.
9. K. Jha, S. Srivastava, A. Jain, "Integrating global and local features for efficient face identification using deep CNN classifier," IEEE 1st International Conference on Device Intelligence, Computing and Communication Technologies (DICCT), 2023, pp. 532–536.
10. K. Jha, S. Srivastava, A. Jain, "A novel speaker verification approach featuring multidomain acoustics based on the weighted city block Minkowski distance," ETRI J. (published online).
11. K. Jha, A. Jain, S. Srivastava, "A secure biometric-based user authentication scheme for cyber-physical systems in healthcare," Int. J. Exp. Res. Rev. 39, 154–169 (2024).
12. Y. Yuan et al., "Attack-defense strategy assisted osprey optimization algorithm for PEMFC parameters identification," Renewable Energy 225, 120211 (2024).
13. Y. Yuan, Q. Shen, W. Xi, S. Wang, J. Ren, J. Yu, Q. Yang, "Multidisciplinary design optimization of dynamic positioning system for semi-submersible platform," Ocean Eng. 285, 115426 (2023).
14. S. A. E. Rahman, A. S. Alluhaidan, "Enhanced multimodal biometric recognition systems based on deep learning and traditional methods in smart environments," Plos One 19(2), e0291084 (2024).
15. V. Vekariya, M. Joshi, S. Dikshit, S. Manju bargavi, "Multi-biometric fusion for enhanced human authentication in information security," Meas.: Sens. 31, 100973 (2024).
16. A. Becerra et al., "Portable student attendance management module for university environment by using biometric mechanisms," Multimed. Tools Appl. 83(1), 1215–1239 (2024).
17. G. R. Naufal, R. Kumala, R. Martin, I. T. A. Amani, Budiharto, "Deep learning-based face recognition system for attendance system," ICIC Express Lett. B: Appl. 12(2), 193–199 (2021).
18. V. Wati et al., "Security of facial biometric authentication for attendance system," Multimed. Tools Appl. 80, 23625–23646 (2021).
19. N. A. Ismail et al., "Web-based university classroom attendance system based on deep learning face recognition," KSII Trans. Internet Inf. Syst. 16(2), 503–523 (2022).
20. X. Zhao et al., "Research on optimization of improved short-term load composite forecasting model based on AM–CNN–Bi–LSTM," AIP Adv. 14(5), 055003 (2024).
21. K. Jha, S. Srivastava, A. Jain, "Cryptanalysis of a biometric based anonymous authentication approach for IoT environment," Int. J. Microsyst. IoT 2(2), 591–597 (2024).
22. G. Revathy et al., "Investigation of E-voting system using face recognition using convolutional neural network (CNN)," Theor. Comput. Sci. 925, 61–67 (2022).
23. K. Jha, A. Jain, S. Srivastava, "Analysis of human voice for speaker recognition: Concepts and advancement," J. Electr. Syst. 20(1s), 582–599 (2024).
24. S. B. Alagarsamy, K. Murugan, "Multimodal of ear and face biometric recognition using adaptive approach Runge–Kutta threshold segmentation and classifier with score level fusion," Wirel. Pers. Commun. 124, 1061–1080 (2022).
25. S. Srivastava, M. Chandra, G. Sahoo, "Speaker identification and its application in automobile industry for automatic seat adjustment," Microsyst. Technol. 25, 2339–2347 (2019).
26. L. Tan, J. Jiang, Digital Signal Processing: Fundamentals and Applications (Academic Press, 2018).
27. A. S. Lateef, M. Y. Kamil, "Facial recognition technology-based attendance management system application in smart classroom," Iraqi J. Comput. Sci. Math. 4(3), 136–158 (2023).
28. S. Salim, W. Ahmad, "Constant Q cepstral coefficients for automatic speaker verification system for dysarthria patients," Circuits Syst. Signal Process. 43(2), 1101–1118 (2024).
29. M. Singhal, K. Shinghal, "Secure deep multimodal biometric authentication using online signature and face features fusion," Multimed. Tools Appl. 83, 30981–31000 (2023).
30. N. Daniel, A. Anitha, "Analysing texture, color and spatial features for face spoof detection with hybrid classification model," Multimed. Tools Appl. 83(13), 37713–37741 (2023).
31. Z. Qin et al., "A survey of identity recognition via data fusion and feature learning," Inf. Fusion 91, 694–712 (2023).
32. C. Dalila, E. A. Omar Badis, B. Saddek, N. A. Amine, "Feature level fusion of face and voice biometrics systems using artificial neural network for personal recognition," Informatica 44(1), 85–96 (2020).
33. S. Yadav et al., "State of the art in energy consumption using deep learning models," AIP Adv. 14(6), 065306 (2024).
34. G. L. Santos et al., "Predicting short-term mobile Internet traffic from Internet activity using recurrent neural networks," Int. J. Netw. Manag. 32(3), e2191 (2022).
35. S. Nainan, V. Kulkarni, "Enhancement in speaker recognition for optimized speech features using GMM, SVM and 1-D CNN," Int. J. Speech Technol. 24, 809–822 (2021).
36. K. Pramilarani, P. Vasanthi Kumari, "Cost based random forest classifier for intrusion detection system in Internet of Things," Appl. Soft Comput. 151, 111125 (2024).
37. B. Yan, C.-T. Li, X. Lu, "JRC: Deepfake detection via joint reconstruction and classification," Neurocomputing 598, 127862 (2024).
38. A. Ephrat et al., "Looking to listen at the cocktail party: A speaker-independent audio-visual model for speech separation," ACM Trans. Graphics 37(4), 1 (2018).
39. M. AlSlaiman, M. I. Salman, M. M. Saleh, B. Wang, "Enhancing false negative and positive rates for efficient insider threat detection," Comput. Secur. 126, 103066 (2023).
40. K. Jha, A. Jain, S. Srivastava, "A contactless speaker identification approach using feature-level fusion of speech and face cues with DCNN," Proc. Eng. Sci. 6(3), 1047–1056 (2024).

---

## Notas para o TCC

*Seção acrescentada nesta tradução; não faz parte do artigo original.*

- **Por que importa:** é a principal referência do projeto para **fusão rosto + voz** em um sistema de presença, e para **detecção de vivacidade** (proteção contra foto ou gravação), os itens E7 e E8 do [documento de lacunas](../lacunas_revisao_bibliografica.md).
- **Fusão no nível das características × no nível da decisão:** o artigo concatena as características antes de classificar. No dispositivo do ônibus, a fusão no nível da decisão (combinar o resultado do modelo de rosto com o do modelo de voz) é mais simples de embarcar e permite trocar um modelo sem retreinar o outro, o que combina com a arquitetura de portas e adaptadores. Na Tabela III, a fusão por pontuação ficou só 2,6 pontos abaixo da proposta.
- **Cuidado com os números:** as características são clássicas (Gabor, LBP, CQCC, formantes), não *embeddings* de redes profundas; a base mistura *deepfakes* com vídeos do YouTube, sem condições de ônibus; há inconsistências nas tabelas; e não há medida de tempo nem teste em hardware embarcado. Use o artigo para a ideia de multimodalidade, não como valor de referência.
- **Referência cruzada:** o artigo cita Surantha e Sugijakko (2024), já na lista de candidatas, como o único sistema de presença com detecção de vivacidade.
