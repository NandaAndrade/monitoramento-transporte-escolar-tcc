# Sistemas de segurança veicular usando reconhecimento facial baseado em Internet das Coisas

> **Tradução integral para o português**, feita para estudo do TCC.
>
> **Original:** ELNGAR, A. A.; KAYED, M. Vehicle Security Systems using Face Recognition based on Internet of Things. *Open Computer Science*, v. 10, p. 17–29, 2020. DOI: [10.1515/comp-2020-0003](https://doi.org/10.1515/comp-2020-0003).
>
> **Licença:** o original é publicado em acesso aberto pela De Gruyter sob a licença [Creative Commons Atribuição 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br), © 2020 A. A. Elngar e M. Kayed. Esta tradução é uma obra derivada: o texto foi traduzido do inglês, as figuras foram substituídas por suas legendas e foram acrescentadas notas da tradução, marcadas como **[N. T.]**, e a seção final "Notas para o TCC". Os autores originais não revisaram nem endossam esta tradução.
>
> **PDF local:** `Downloads/Referencias/elngar_2020_seguranca_veicular_reconhecimento_facial_iot.pdf`

---

**Ahmed A. Elngar\* e Mohammed Kayed**
Faculdade de Computação e Inteligência Artificial, Universidade de Beni-Suef, Egito.
Recebido em 15 set. 2019; aceito em 12 nov. 2019.

## Resumo

Atualmente, o setor automotivo é uma das aplicações mais em evidência, já que os veículos podem se tornar inteligentes com o uso da tecnologia de IoT. Infelizmente, porém, esses veículos sofrem com muitos crimes. Por isso, tornou-se um grande desafio para a IoT evitar esses crimes cometidos por ladrões profissionais. Este artigo apresenta uma proposta de desenvolvimento de um sistema de proteção e alarme veicular que usa autenticação biométrica baseada em tecnologia IoT. Para as questões de segurança do veículo, o sistema proposto, VSS-IoT, dá acesso completo apenas ao motorista autorizado do veículo, com base na interface de uma placa de desenvolvimento Raspberry Pi 3 Model B+, uma Picamera, um sensor PIR e um smartphone. Assim, se o sistema detectar uma pessoa não autorizada dentro do veículo, ele notifica e envia a imagem dessa pessoa ao dono do veículo e/ou a uma estação policial pela Internet, além da localização, caso o veículo seja roubado ou danificado. O sistema proposto foi testado em duas bases de dados: a base ORL e a nossa própria base. Os resultados experimentais do VSS-IoT mostraram acurácia de 98,2% na base ORL e de 99,6% na nossa base. Além disso, o VSS-IoT eleva a sensibilidade para 97,7%, o que é importante para o tempo real. Os resultados também mostraram que o sistema proposto levou menos tempo, 0,152 s, sob diferentes condições de iluminação, quando o valor do limiar é 3 × 10³ e 3,50 × 10³. Portanto, o VSS-IoT é muito robusto e confiável para reconhecimento facial quando implantado em um processador de baixo consumo.

**Palavras-chave:** Internet das Coisas, reconhecimento facial, Haar cascade, análise de componentes principais, sistemas de segurança veicular.

## 1 Introdução

Nos últimos anos, a popularidade do setor automotivo vem crescendo no mundo todo [1]. Infelizmente, porém, há um aumento exponencial dos crimes envolvendo veículos [2]. Hoje, a maioria dos veículos é controlada por chaves mecânicas, cartões de segurança e senha/padrão. Mas, com o desenvolvimento das tecnologias de IoT e de muitos mecanismos embarcados, os sistemas de segurança veicular vêm melhorando continuamente [3]. Essas melhorias dependem dos requisitos dos donos dos veículos e das estações policiais [4]. Elas não tratam apenas do furto do conteúdo do veículo, mas também da perda do próprio veículo e dos requisitos de segurança pessoal do dono [5].

Existem muitas técnicas conhecidas de identificação e verificação baseadas em biometria. Impressões digitais, características faciais e íris têm sido empregadas em diversas aplicações de segurança. O reconhecimento facial é considerado uma boa técnica biométrica para sistemas de segurança e alarme veicular, porque se baseia nas informações das características do rosto humano e pode funcionar sob condições diferentes [6]. Por isso, a maioria das técnicas de reconhecimento facial foi desenvolvida para alcançar uma taxa de discriminação maior [7].

Como o processo de reconhecimento facial envolve cálculos complexos, este artigo propõe um sistema VSS-IoT confiável, baseado em um processador de baixo consumo, como proteção contra o furto de veículos [8]. O sistema converte as imagens capturadas pela câmera USB instalada no veículo em imagens em tons de cinza para detectar e reconhecer rostos em tempo real. A combinação do algoritmo AdaBoost com o classificador Haar Cascade melhora a acurácia da detecção de rostos [9]. Em seguida, o sistema proposto emprega o algoritmo PCA para reconhecer os rostos dos motoristas [10].

Este artigo tem como objetivo empregar o método proposto de detecção e reconhecimento facial em sistemas de segurança veicular por meio da interface com a tecnologia IoT, com o apoio de alguns sensores. O sistema se baseia na placa de desenvolvimento Raspberry Pi 3 Model B+ e em um smartphone para implementar a ideia. A placa Raspberry Pi 3 Model B+ pode ser ligada a um sensor de movimento, a um servomotor e a uma câmera USB. Além disso, a Raspberry Pi 3 Model B+ pode ser programada para enviar um e-mail a um servidor de e-mail definido, e para buscar e enviar dados a um servidor Firebase conectado a um aplicativo Android, para análise de vídeo em tempo real.

Com esse sistema, quando o rosto de uma pessoa não autorizada é encontrado, o sistema o analisa e envia a imagem dessa pessoa ao dono do veículo e/ou à estação policial pelas redes IoT. Os resultados experimentais do VSS-IoT mostraram acurácia de 98,2% na base ORL e de 99,6% na nossa base. Além disso, o VSS-IoT eleva a sensibilidade para 97,7%, o que é importante para o tempo real. Os resultados também mostram que o sistema proposto levou menos tempo, 0,152 s, sob diferentes condições de iluminação, quando o limiar vale 3 × 10³ e 3,50 × 10³, em comparação com outros sistemas.

A economia de energia é uma das questões mais importantes na construção de sistemas inteligentes de segurança veicular. Assim, o processador de baixo consumo se torna um tema interessante para ser investigado e avaliado quanto ao desempenho do reconhecimento facial. O sistema proposto apresenta baixo uso de CPU e de memória, 76% e 53,5%, respectivamente, dependendo da resolução da câmera usada. **[N. T.: na Tabela 10 e na Conclusão, 53,5 aparece em MB, não em %.]**

O restante do artigo está organizado da seguinte forma: a Seção 2 apresenta a formulação do problema. A Seção 3 apresenta uma revisão da literatura. A Seção 4 apresenta o sistema proposto (VSS-IoT) para segurança veicular. A Seção 5 apresenta os resultados da implementação e sua análise. Por fim, a Seção 6 traz as considerações finais.

## 2 Formulação do problema

Impedir o acesso de uma pessoa não autorizada ao sistema de segurança do veículo é um problema, mas o problema real é como identificar o rosto dessa pessoa. A maioria dos sistemas para veículos roubados ajuda a recuperá-los, mas o crime já aconteceu. Por isso, deve-se desenvolver um bom sistema veicular que ofereça segurança com base em novas tecnologias, como a Internet das Coisas (IoT) [11]. O sistema do veículo deve empregar autenticação de usuário para controle de acesso, usando autenticação biométrica baseada em IoT em tempo real. Além disso, o sistema deve monitorar o veículo em busca de qualquer atividade suspeita em seu interior [12]. O sistema de vigilância deve manter o veículo seguro, notificando o motorista autorizado pelo aplicativo móvel ou por e-mail, caso qualquer pessoa não autorizada ou qualquer intrusão tente acessar o sistema de segurança do veículo. O sistema também deve oferecer recursos extras, como a localização do veículo, no mesmo hardware, sem aumentar a complexidade nem o custo [13].

Seja $z_t$ o conjunto de valores dos sensores do sistema de vigilância adquiridos no instante $t$:

$$z_t(a) = D_t[b_t](a), \quad \forall a \in A \tag{1}$$

em que $D_t$ denota um fator de transformação do registro original $b_t$, e $a \in z^2$ indica os valores dos sensores que pertencem ao registro regular $A \subset z^2$. Enquanto não houver atividade suspeita:

$$D_t[b_t](a) = b_t(a) + \eta_t(a), \quad \forall a \in A \tag{2}$$

em que $\eta_t$ é uma variável aleatória que estima os valores de ruído do registro, e os $b_t$ são adquiridos do mesmo sensor, embora em geral $b_t \neq b_{t-1}$, porque os valores do registro do sistema de vigilância mudam.

Quando, no instante $\tau^*$, uma perturbação externa introduz algo suspeito, o registro $b_t$ é degradado por uma pessoa não autorizada ou por uma atividade suspeita desconhecida, e $z_t$ passa a ser:

$$D_t[b_t](a) = \int b(e)\, h_t(a, j)\, dj + \eta_t(a), \quad \forall a \in A,\ t \succeq \tau^* \tag{3}$$

em que $h_t(a, j)$ é a função de espalhamento de valores no valor $a \in A$.

O VSS-IoT proposto é um sistema usado para analisar uma sequência $\{z_t,\ t = 1, \ldots, \text{número de sensores}\}$ para detectar e reconhecer qualquer rosto não autorizado ou intruso, e o instante $\tau^*$ em que a atividade suspeita ocorre, como na Equação 3. Supomos que $T_0$ valores livres de atividade suspeita são fornecidos para o treinamento.

## 3 Revisão da literatura

A IoT executa funções inteligentes que ajudam a evitar o furto de veículos [14]. Muitos autores vêm trabalhando em sistemas de segurança veicular para oferecer os melhores mecanismos, tratando não só do furto do conteúdo do veículo, mas também da perda do veículo e dos requisitos de segurança pessoal do dono. Em seus trabalhos, eles desenvolveram sistemas de segurança veicular baseados em "autenticação biométrica", como reconhecimento de olho, de dedo, de rosto etc. [15] [16]. Esta seção descreve algumas contribuições relevantes propostas nos últimos anos.

Os autores de [1] propõem um sistema embarcado antifurto e de vigilância do motorista. Eles usaram autenticação biométrica para acessar o veículo. Os autores afirmam que o sistema usa o algoritmo LBPH para reconhecimento facial e mostraram que o sistema era simples e dava melhores resultados sob várias condições de luz.

Conforme [17], os autores apresentaram um sistema embarcado de segurança veicular chamado "POLLUX". A segurança do sistema se baseia em tecnologia de visão de máquina. Ele funciona como um novo nível de prevenção contra furto, que protege o veículo sem ser intrusivo para os motoristas. O sistema usou uma rede neural (NN) para a detecção de rostos e máquinas de vetores de suporte (SVM) para o reconhecimento facial.

O principal objetivo do trabalho [18] é oferecer um sistema de segurança avançado no veículo. O programa consiste em uma senha associada a um programa de detecção e reconhecimento facial, um módulo GSM e uma plataforma de controle. O sistema de detecção de rostos usa o algoritmo de padrões binários locais (LBP) otimizado para detectar o rosto dos usuários. Além disso, o sistema usou o algoritmo PCA para o reconhecimento facial.

Os autores de [6] afirmam ter proposto um sistema de segurança baseado em comunicação sem fio e em um módulo Bluetooth. Eles tentaram usar o módulo GSM para enviar mensagens. O dono do veículo pode controlar o motor/ignição e desligá-lo a qualquer momento. Os autores também supõem que o sistema possa usar uma senha por teclado (com no máximo 3 tentativas), que controla a segurança da trava da porta do veículo e o uso do cinto de segurança. Além disso, o controlador é conectado a um módulo Bluetooth.

Segundo [7], os autores propuseram um arcabouço de baixo custo e expansível para um sistema embarcado inteligente de segurança veicular. Os autores afirmam que o sistema consiste em um subsistema de detecção de rostos, um módulo GPS, um módulo GSM e uma plataforma de controle. O algoritmo Haar cascade otimizado é usado no subsistema de detecção de rostos. O sistema também pode reconhecer rostos no veículo e disparar um alarme silencioso.

Os autores de [19] apresentaram o projeto e o desenvolvimento de um sistema de reconhecimento facial. Eles usam um Haar cascade para detectar rostos em uma imagem. Em seguida, o sistema emprega redes neurais artificiais (ANN) para o reconhecimento facial. Os autores afirmam que, nos experimentos, o sistema reconhece rostos humanos com acurácia de 88,6%.

Em [12], os autores afirmam usar um modelo de múltiplos estágios para a detecção de rostos, integrando o algoritmo de Viola e Jones, filtros de Gabor e análise de componentes principais (PCA). Em seguida, usam redes neurais artificiais (ANN) para o reconhecimento facial, com acurácia de 90,3%.

## 4 O sistema de segurança veicular proposto, VSS-IoT

Esta seção descreve a ideia por trás do VSS-IoT proposto. O principal objetivo do sistema proposto é detectar e reconhecer os rostos de ladrões profissionais. Além disso, o sistema proposto oferece baixo custo, simplicidade e facilidade de uso, o mais importante para implementar um sistema embarcado de segurança veicular em tempo real. Assim, o sistema deve primeiro obter a identidade do motorista dono do veículo e então autorizá-lo a acessar o sistema do veículo. O sistema proposto combina técnicas biométricas, dispositivos embarcados e tecnologias IoT para projetar um sistema de segurança veicular eficaz, com vigilância e alerta. O sistema pode ser feito de forma eficiente em duas partes: o projeto da arquitetura de hardware e o projeto da arquitetura de software.

A Figura 1 apresenta o fluxograma básico de todo o sistema de segurança veicular. Ela ilustra a sequência de eventos desde a intrusão até o envio do alerta.

> [Figura 1: Fluxograma básico de todo o sistema VSS-IoT.]

### 4.1 Arquitetura de hardware do sistema

A arquitetura de hardware do VSS-IoT proposto é composta por: controlador Raspberry Pi 3 Model B+, sensor de movimento PIR, modem USB 3G, módulo de câmera USB para Pi, cartão microSD, servomotor, fonte de alimentação, dispositivo móvel do dono, estação policial e unidade de controle do veículo. Os componentes propostos são conectados com e sem fio: a estação policial e os terminais do dono são conectados sem fio ao controlador Raspberry Pi 3 Model B+, e todos os demais dispositivos são ligados por meio cabeado, como mostra a Figura 2.

> [Figura 2: Arquitetura de hardware do VSS-IoT.]

- **Raspberry Pi 3 Model B+:** este modelo tem muitas vantagens sobre os outros, já que tem muitas portas USB e pinos GPIO. Além disso, usa o sistema operacional "Raspbian", que tem ótima integração com o hardware e uma interface gráfica com ferramentas de desenvolvimento.
- **Conexão com a Internet:** é um componente necessário neste trabalho, para que a Raspberry Pi 3 Model B+ possa se comunicar por protocolos de rede IoT. A arquitetura da Figura 2 mostra que foi necessário mudar o endereço IP da Raspberry Pi 3 Model B+ de estático para dinâmico. Isso foi feito editando o arquivo de interfaces de rede com o comando `sudo nano /etc/network/interfaces`.
- **Câmera USB:** câmera feita especificamente para a Raspberry Pi 3 Model B+. Ela foi ligada à placa pela porta USB, que é extremamente rápida. Para configurar e habilitar a câmera, foi executado na linha de comando da Raspberry Pi 3 Model B+ o comando `sudo apt-get install fswebcam`.
- **Sensor infravermelho passivo:** o dispositivo usado foi o sensor infravermelho passivo HC501SR. O alcance de detecção é de 7 metros com ângulo de cone de 140 graus. Tem um tempo de atraso de 16 s, ajustável. A temperatura ambiente de operação é de 253 K a 323 K. Ele foi alimentado diretamente pela Pi, pelo pino de 5 V de corrente contínua. Sua saída foi ligada como entrada a um pino GPIO programável.
- **Servomotor:** componente usado para controlar o injetor de combustível. Foi projetado para ser acionado pelo sistema quando uma pessoa não autorizada é detectada.

### 4.2 Inicialização e configuração do sistema

Esta subseção trata da inicialização e da configuração do sistema, em que todos os nós são estabelecidos para se conectar. A rede do sistema proposto deve usar o IEEE 802.15.4 na camada física, para prover comunicação sem fio, de modo que os bits de dados, depois de convertidos em sinais, possam ser transmitidos ao dono do veículo e/ou à estação policial. Na camada de enlace, o 6LoWPAN é usado como camada de adaptação, onde é feito o ajuste do IPv6 ao IEEE 802.15.4. O protocolo IPv6 é usado para endereçamento e roteamento dos dados, permitindo atribuir a cada nó um endereço IPv6 único. A camada seguinte é a de transporte, em que o UDP é usado para carregar os dados. Por fim, na camada de aplicação, é usado o protocolo CoAP. A rede do sistema proposto também se conecta a outras redes por Wi-Fi. O sistema também executa as seguintes tarefas:

- **Importação de bibliotecas e pacotes Python:** essas bibliotecas são predefinidas e ajudam os módulos de interface a funcionar corretamente.
- **Ajuste e configuração da câmera USB:** depois dessas configurações da câmera USB, o sistema foi reiniciado, para garantir que a câmera recebesse espaço suficiente na memória. A câmera tira imagens de 5 MP e tem resolução de 640 × 480. Foi usado o comando `fswebcam image.jpg` sobre a imagem.
- **Ajuste dos GPIO e inicialização dos pinos:** o canal foi definido com a numeração de canais BCM. O canal do pino do infravermelho passivo foi configurado em modo de leitura; assim, para ler o valor de qualquer pino GPIO, basta digitar `GPIO.input(channel)`. Já o canal do LED foi configurado em modo de escrita; para acionar o canal do pino GPIO, digita-se `GPIO.output(channel, status)`.
- **Geração e envio de e-mail:** depois de configurar o sistema, é necessário gerar e enviar o e-mail ao assinante predefinido. O pacote MIME (*Multipurpose Internet Mail Extension*) foi usado para gerar o e-mail com anexo. O MIME suporta caracteres e anexos não textuais (áudio, vídeo, programas etc.). Além disso, o programa SMTP (*Simple Mail Transfer Protocol*) é usado para entregar o e-mail da Raspberry Pi 3 Model B+ ao servidor de e-mail configurado. Isso pode ser resumido no algoritmo abaixo:

```
Inicia o sistema.
Envia e-mail com o IP atribuído na inicialização a um servidor de e-mail.
Verifica o estado do pino GPIO.
SE (a entrada do pino GPIO está em nível baixo)
    ENTÃO a saída do pino GPIO 13 fica em nível baixo e o sistema fica ocioso.
SENÃO a entrada do pino GPIO passa subitamente para nível alto.
    ENTÃO ocorre um evento de interrupção.
FIM SE
ENQUANTO (o valor da entrada GPIO está em nível alto)
    Coloca a saída do pino GPIO 13 em nível alto.
    Chama a função que liga a câmera.
    A câmera detecta e reconhece o rosto.
    SE (uma pessoa autorizada é detectada e reconhecida)
        ENTÃO abre o servomotor.
    SENÃO uma pessoa não autorizada é detectada e reconhecida.
        Fecha o servomotor e verifica a Internet.
    FIM SE
    SE (há Internet disponível)
        ENTÃO (fecha o servomotor e gera a mensagem MIME com anexo e a notificação móvel).
        Chama o servidor SMTP para enviar o alerta com anexo.
        Chama o Firebase e o Pusher para enviar a notificação.
        Limpa os GPIO e repete o laço.
    SENÃO verifica de novo após 0,5 segundo.
    FIM SE
FIM ENQUANTO
```

Essa sequência de eventos é detalhada no diagrama de blocos da Figura 3.

> [Figura 3: Inicialização e configuração do sistema.]

### 4.3 Projeto de software do sistema VSS-IoT

Esta subseção dá uma visão geral do projeto de software do nosso sistema VSS-IoT, que se baseia nos principais módulos de detecção e reconhecimento facial. O sistema foi desenvolvido na placa Raspberry Pi 3 Model B+, com a versão mais recente do sistema operacional "Raspbian", conectada a alguns sensores e atuadores. Se um ladrão tentar acessar a carroceria do veículo, o sistema de segurança é ligado automaticamente. Em seguida, todos os sensores do sistema de segurança são acionados: se o sensor de movimento PIR, considerado a primeira linha de defesa, detectar qualquer movimento repentino, ele passa do estado ocioso para o ativo. Além disso, quando o ladrão se senta no banco do motorista, a imagem do seu rosto é capturada por uma câmera USB oculta, localizada no alto, à frente do motorista, de forma a capturar a imagem com facilidade. Depois de capturada, a imagem é enviada ao dispositivo controlador e convertida para um formato compatível. O controlador então compara $f_n$ (que representa a quantidade de pixels da imagem capturada) com $f_{n-1}$ (que representa a quantidade de pixels das imagens do dono do veículo previamente armazenadas no seu banco de imagens). Se houver correspondência, o controlador permite que o dono acesse o sistema do motor do veículo; caso contrário, o controlador identifica a imagem capturada como de uma pessoa não autorizada e não lhe dá acesso ao sistema do veículo. O sistema de segurança então notifica o dono e/ou a estação policial por diferentes canais, como aplicativo móvel e e-mail. Todas essas mudanças de estado interrompem o controlador imediatamente, e ele comanda o controle do motor do veículo, desligando-o a qualquer instante. A Figura 4 mostra algumas fases funcionais, cujas responsabilidades são descritas abaixo.

> [Figura 4: Projeto do sistema de software do VSS-IoT.]

#### 4.3.1 Fase de aquisição e pré-processamento

O objetivo da aquisição de imagens é obter, em tempo real, as imagens de vídeo do rosto do motorista com uma câmera IP, e armazená-las no banco de dados para os processos de treinamento e teste. Nesta fase, as imagens são normalizadas e realçadas para melhorar a capacidade das fases de detecção e reconhecimento. Para isso, algumas propriedades métricas são obtidas em condições diferentes, como clima, com ou sem óculos, gênero e idade, o que ajuda a produzir características distinguíveis na fase de processamento de imagem. Depois de adquiridas as imagens, o sistema enfrenta alguns desafios, como iluminação instável, fundo variável e outros obstáculos. Por isso, o pré-processamento normaliza a intensidade, o tamanho e o formato da imagem. O pré-processamento de imagem é uma técnica para melhorar as imagens/sinais brutos recebidos das câmeras/sensores instalados nos veículos. Os passos de pré-processamento a implementar são:

- Ligar a câmera e configurá-la para capturar o fluxo de vídeo.
- Capturar um quadro do fluxo de vídeo. Se o quadro for capturado, continuar o processo.
- Caso contrário, parar e inicializar o quadro como quadro atual.
- Conversão para tons de cinza: imagem em tons de cinza significa que a informação de cor da imagem é descartada e a imagem é convertida para um formato representado por um número de 0 a 255 em decimal, ou de 00000000 a 11111111 em binário.

  *Definição:* seja $V$ um conjunto de valores para qualquer imagem, e seja uma imagem com valores de $E$ em $V$. Então $I: E \to V$, em que $I(x)$ é chamado de valor do pixel $x$ em $I$. Seja $K$ o conjunto de todas as imagens com valores inteiros em $E$. Assim, $I(k)$ também é chamado de valor do pixel em tons de cinza da imagem.

- Desfoque da imagem: o conceito de desfoque significa que a imagem parece mais detalhada se conseguirmos perceber corretamente todos os objetos e suas formas nela. O desfoque pode ser obtido de muitas maneiras. A técnica de desfoque gaussiano (também chamada de suavização gaussiana) é usada para desfocar a imagem e reduzir o ruído. Além disso, a suavização gaussiana é usada como etapa de pré-processamento para realçar estruturas da imagem em diferentes escalas. A equação de uma função gaussiana é:

  $$G(x) = \frac{1}{\sqrt{2\pi\sigma^2}}\, e^{-\frac{x^2}{2\sigma^2}} \tag{4}$$

- Capturar outro quadro e repetir os passos acima.
- Verificar se o limiar de pixels é suficiente para chamar a função de movimento detectado.
- Então desenhar um retângulo em volta da região em que o movimento foi detectado.

#### 4.3.2 Fase de detecção de rostos

Várias abordagens de detecção de rostos foram desenvolvidas nos últimos anos. Aplicações como sistemas de vigilância e classificação de gênero usam a tecnologia de detecção de rostos como parte da identificação facial. As técnicas de detecção de rostos se concentram em determinar a parte frontal dos rostos humanos, como posição e tamanho, em qualquer imagem digital. Assim, detectam apenas o rosto e tratam o restante da imagem como fundo. Este artigo apresenta um sistema de segurança veicular robusto que usa a técnica rápida de detecção de rostos Haar cascade. Ela é considerada um algoritmo de aprendizado de máquina para detecção de objetos, usado para identificar objetos em imagens ou vídeos com base no conceito de características de Haar, proposto por Viola e Jones [20]. O principal objetivo do classificador Haar cascade é rejeitar as regiões da imagem digital que provavelmente não contêm um rosto. O algoritmo se divide em quatro etapas:

- **Seleção das características de Haar:** a etapa central do classificador Haar cascade é coletar as características de Haar. Uma característica de Haar considera grupos retangulares adjacentes de pixels em uma posição específica de uma região de detecção. Em seguida, soma as intensidades de todos os pixels de cada região e calcula a diferença entre essas somas para determinar regiões relativamente claras e escuras, isto é:

  $f(x) = \text{Soma}_{\text{retângulo preto}}(\text{intensidades dos pixels}) - \text{Soma}_{\text{retângulo branco}}(\text{intensidades dos pixels})$

  Alguns tipos diferentes de características de Haar aparecem na Figura 5.

  > [Figura 5: Diferentes tipos de características de Haar.]

- **Criação de imagens integrais:** para calcular essas características rapidamente, constrói-se a imagem integral. A Equação 5 mostra o cálculo da soma de todos os pixels dentro de um retângulo qualquer. São necessários apenas quatro valores de pixel, a partir do pixel do canto superior esquerdo $(x, y)$:

  $$p(x, y) = \sum_{x' \le x,\ y' \le y} i(x', y') \tag{5}$$

- **Treinamento com AdaBoost:** o passo seguinte na construção do classificador Haar cascade, para selecionar as características de Haar importantes, é usar o algoritmo de aprendizado AdaBoost. Ele é usado para detectar os rostos na imagem digital extraindo as melhores características. Uma combinação de classificadores fracos pode produzir um classificador forte, como na equação:

  $$S(x) = a_1 w_1 + a_2 w_2 + \ldots + a_n w_n \tag{6}$$

  em que os $w_n$ são $n$ classificadores fracos, definidos na Equação 7, usados para construir o classificador forte $S(x)$:

  $$w_j = \begin{cases} 1 & P_j f_j \le P_j \theta_j \\ -1 & \text{caso contrário} \end{cases} \tag{7}$$

  em que $P_j$ é a direção do viés, $\theta_j$ é o limiar e $f_j$ é uma função característica.

- **Classificadores em cascata:** o classificador Haar cascade é uma série de estágios. Cada estágio contém um classificador fraco treinado para ser forte. Se a imagem passar por todos os estágios, ela é considerada um rosto humano; caso contrário, não é um rosto humano.

#### 4.3.3 Fase de reconhecimento facial

O reconhecimento facial é considerado uma fase importante em sistemas de segurança. Muitas técnicas buscam melhor reconhecimento em tempo real quando aplicadas em computadores de alta velocidade. Felizmente, porém, o processamento em tempo real do reconhecimento facial em sistemas de segurança veicular pode não ser obrigatório quando os crimes são cometidos na rua. Assim, o sistema de segurança veicular tem tempo suficiente para verificar o motorista. Como o reconhecimento facial no sistema de segurança veicular é implementado em um processador de baixo consumo, como a placa Raspberry Pi 3 Model B+, escolher um algoritmo adequado é muito importante. Este trabalho investiga o uso do algoritmo de análise de componentes principais (PCA) [21] para reconhecer rostos em um processador de baixo consumo. A PCA é um método matemático expresso como uma transformação $W^t$ de imagens faciais de alta dimensão $n$ em poucas componentes principais $m$, chamadas de *eigenfaces*, com $m < n$. No nosso sistema VSS-IoT, temos 10 veículos, cada um com 5 motoristas autorizados. Para cada motorista, o sistema reúne 10 imagens para serem treinadas como *eigenfaces*. Essas imagens foram normalizadas para 64 × 64 pixels. Os resultados do treinamento são salvos e ordenados em um arquivo de modelo, a partir dos de maior autovalor. O algoritmo PCA no sistema segue os passos:

- Passo 1: seja $I$ uma imagem de tamanho $N \times N$.
- Passo 2: converter $I$ em $\Gamma$ de tamanho $P \times 1$, com $P = N \times N$.
- Passo 3: suponha o conjunto de treino $\Gamma' = [\Gamma'_1, \Gamma'_2, \ldots, \Gamma'_M]$.
- Passo 4: calcular a média $\psi = \frac{1}{M}\sum_{i=1}^{M} \Gamma'_i$.
- Passo 5: calcular a diferença de cada rosto, $\Phi_i = \Gamma'_i - \psi$; a matriz de diferenças é definida como $A = [\Phi_1, \Phi_2, \ldots, \Phi_M]$.
- Passo 5 **[N. T.: numeração repetida no original]**: calcular a matriz de covariância $C = AA^T$, de tamanho $P \times P$; depois, reduzir o tamanho usando $L = A^TA$, de tamanho $M \times M$.
- Passo 6: calcular os autovetores por $A^TAX_i = \lambda_i X_i$, em que $U_i = AX_i$ é o autovetor e $\lambda_i$ é o autovalor.
- Passo 7: calcular a imagem facial projetada por $\Omega_k = U_k^T \Phi_i$.
- Passo 8: para a imagem de teste $\Gamma'_t$, usar $\Phi_t = \Gamma'_t - \psi$.
- Passo 9: calcular a projeção da imagem de teste por $\Omega = U_k^T \Phi_t$.
- Passo 10: calcular a distância euclidiana para achar a menor distância entre a imagem de teste e as imagens de treino, usando $\varepsilon_k^2 = \lVert \Omega - \Omega_k \rVert^2$. Se $\varepsilon_{k(\min)} \ge \Theta$, a imagem é desconhecida; se $\varepsilon_{k(\min)} \le \Theta$, o rosto é conhecido.

#### 4.3.4 Fase de rotulação do rosto

O resultado da fase de reconhecimento é usado nesta fase. Como a imagem é convertida para forma binária, esse rótulo é usado para avaliar um valor específico e compará-lo com o valor do nome de uma pessoa no banco de dados do Firebase. Se o valor corresponder, o nome é retornado com sucesso. Caso contrário, o sistema retorna o valor predefinido "nome desconhecido", como mostra a Figura 6.

> [Figura 6: Rosto de pessoa autorizada reconhecido com sucesso.]

### 4.4 Controle por aplicativo móvel e notificação por e-mail

Nesta subseção, a Raspberry Pi 3 Model B+ se conecta ao aplicativo Android pelo servidor Firebase, para criar um aplicativo móvel para a pessoa que é o motorista autorizado. A Raspberry Pi 3 Model B+ envia dados ao banco de dados Firebase, e o Pusher executa ações como enviar uma notificação (a imagem do ladrão com a mensagem) ao aplicativo Android chamado "Car Locked", para alertar o dono do veículo, como mostra a Figura 7.

Os passos a seguir mostram como criar esse aplicativo móvel:

- criar o código Java e conectá-lo ao banco de dados Firebase, como mostra a Figura 8;
- projetar a interface de usuário em XML, como mostra a Figura 9.

Por outro lado, para permitir o envio de notificações por e-mail à estação policial, usa-se o SMTP (*Simple Mail Transfer Protocol*), um programa que permite a um sistema enviar e receber e-mails de um computador para um servidor de e-mail. Assim, o SMTP é um protocolo ideal para situações em que alertas precisam ser enviados junto com a imagem dos ladrões.

> [Figura 7: Controle pelo aplicativo móvel.]
> [Figura 8: Código Java com Firebase.]
> [Figura 9: Projeto da interface de usuário do aplicativo móvel.]

## 5 Resultados da implementação e análise de segurança

O VSS-IoT proposto foi avaliado em duas bases de rostos: a base ORL [22], mostrada na Figura 10, e a nossa base, coletada em 10 veículos, cada um com 5 motoristas autorizados. Para cada motorista autorizado, o sistema reúne 10 imagens para serem treinadas como *eigenfaces*. Em seguida, cada motorista autorizado foi testado 100 vezes sem óculos e 100 vezes com óculos. Além disso, para cada veículo, testamos 5 pessoas não autorizadas, cada uma testada 100 vezes. Todos os experimentos foram realizados em um processador Intel Core i7 de 4 GHz com 4 GB de RAM. Os experimentos foram implementados em ambiente Python com banco de dados Firebase e o microcontrolador Raspberry Pi 3 Model B+, e em Java, usando alguns sensores.

> [Figura 10: Algumas amostras da base ORL.]

### 5.1 Medidas de desempenho

A eficácia do reconhecimento do VSS-IoT proposto é medida em termos de acurácia, sensibilidade, especificidade e precisão, calculadas a partir dos valores de verdadeiros positivos (TP), verdadeiros negativos (TN), falsos positivos (FP) e falsos negativos (FN), como mostram as Equações 8, 9, 10 e 11, respectivamente. A Equação 12 mostra como as Equações 9 e 10 afetam a acurácia, ao serem multiplicadas pelas Equações 13 e 14.

$$\text{Acurácia} = \frac{TP + TN}{TP + TN + FP + FN} \tag{8}$$

$$\text{Sensibilidade} = \frac{TP}{TP + FN} \tag{9}$$

$$\text{Especificidade} = \frac{TN}{TN + FP} \tag{10}$$

$$\text{Precisão} = \frac{TP}{TP + FP} \tag{11}$$

$$\text{Acurácia} = \text{Prevalência} \times \text{Sensibilidade} + (1 - \text{Prevalência}) + \text{Especificidade} \tag{12}$$

**[N. T.: a expressão correta é $(1 - \text{Prevalência}) \times \text{Especificidade}$; o original traz "+" no lugar do segundo "×".]**

$$\text{Prevalência} = \frac{\text{Positivos}}{\text{Positivos} + \text{Negativos}} \tag{13}$$

$$1 - \text{Prevalência} = \frac{\text{Negativos}}{\text{Positivos} + \text{Negativos}} \tag{14}$$

em que:

- **Verdadeiros negativos (TN):** número de eventos normais rotulados corretamente como normais.
- **Falsos positivos (FP):** número de eventos normais previstos como anormais.
- **Falsos negativos (FN):** número de eventos anormais previstos incorretamente como normais.
- **Verdadeiros positivos (TP):** número de eventos anormais previstos corretamente como anormais.
- **Prevalência:** razão entre o número de amostras positivas e o total de amostras.
- **1 − Prevalência:** razão entre o número de amostras negativas e o total de amostras.

### 5.2 Resultados dos experimentos

Neste sistema, o classificador Haar cascade foi aplicado para a detecção de rostos e a PCA para o reconhecimento facial. Os parâmetros usados no nosso sistema são:

- **Taxa de aumento da escala:** este parâmetro busca equilibrar o número de passadas do detector Haar e a acurácia. Se o valor for alto, o detector roda rápido, mas perde rostos. Assim, o valor do parâmetro deve ser 1,2, entre os valores 1,1, 1,2, 1,3 e 1,4, o que leva a um número moderado de passadas e a melhor acurácia.
- **Limiar mínimo de vizinhos:** o objetivo deste parâmetro é encontrar o limiar mínimo de vizinhos que decide se um grupo de retângulos é descartado ou mantido como rosto. O parâmetro varia de 0 a 10. Neste trabalho, escolhemos o mínimo de vizinhos com maior probabilidade de ser identificado como "rosto".
- **Escala mínima de detecção:** o parâmetro seguinte define o menor tamanho de rosto, alterando os valores do classificador Haar cascade no arquivo XML. Para obter os melhores resultados, definimos esse valor como 25 × 25 nos experimentos. É preciso garantir que a razão entre largura e altura seja a mesma do padrão.
- **Limiar:** chama-se de limiar o valor máximo da distância, calculada pela função de distância euclidiana, entre os valores das imagens de teste e das imagens de treino. Todos os experimentos foram feitos com diferentes valores de limiar, com 5 motoristas autorizados, 100 vezes sem óculos e 100 vezes com óculos. O sistema também foi avaliado com 5 pessoas não autorizadas, 100 vezes. Nos nossos experimentos, a taxa de reconhecimento aumentou ajustando o valor do limiar por tentativa e erro, usando $\Theta_{\text{novo}} = 0{,}8 \times \Theta_{\text{antigo}}$ do valor máximo das menores distâncias euclidianas de cada imagem às demais (ver subseção 4.3.3).

Os resultados dos experimentos na nossa base são mostrados a seguir, em que CR denota reconhecimento correto, FR denota reconhecimento falso e NotR denota não reconhecido.

**Tabela 1:** Reconhecimento correto do motorista autorizado nº 1, sem e com óculos.

| Limiar | Sem óculos: CR | FR | NotR | Com óculos: CR | FR | NotR |
|---|---|---|---|---|---|---|
| 1,5 × 10³ | 92 | 1 | 7 | 87 | 3 | 10 |
| 2 × 10³ | 92 | 2 | 6 | 89 | 5 | 6 |
| 2,25 × 10³ | 94 | 0 | 6 | 92 | 0 | 8 |
| 2,50 × 10³ | 96 | 1 | 3 | 91 | 0 | 9 |
| 2,75 × 10³ | 94 | 1 | 5 | 92 | 5 | 3 |
| 3 × 10³ | 100 | 0 | 0 | 98 | 2 | 0 |
| 3,50 × 10³ | 100 | 0 | 0 | 99 | 0 | 1 |
| 4 × 10³ | 99 | 0 | 1 | 77 | 13 | 10 |
| 4,50 × 10³ | 87 | 8 | 5 | 70 | 17 | 13 |
| 5 × 10³ | 80 | 15 | 5 | 75 | 12 | 13 |

Como se observa na Tabela 1, um bom valor de limiar é 3 × 10³ e 3,50 × 10³, que dá um reconhecimento facial altamente preciso, de 100% e 99%, para o motorista autorizado nº 1 sem e com óculos, respectivamente. Além disso, à medida que o limiar aumenta, crescem o reconhecimento falso e o não reconhecimento, o que significa desempenho ruim.

A Tabela 2 mostra que o melhor desempenho para o motorista autorizado nº 2 é obtido quando o limiar vale 3 × 10³ e 3,50 × 10³.

A Tabela 3 mostra que o valor excelente do limiar foi 3 × 10³ e 3,50 × 10³, que dá o melhor desempenho e um reconhecimento facial correto eficiente para o motorista autorizado nº 3.

A Tabela 4 mostra que o valor de limiar de maior acurácia foi 3 × 10³ e 3,50 × 10³ para reconhecer corretamente o motorista autorizado nº 4, mesmo sem e com óculos.

**Tabela 2:** Reconhecimento correto do motorista autorizado nº 2, sem e com óculos.

| Limiar | Sem óculos: CR | FR | NotR | Com óculos: CR | FR | NotR |
|---|---|---|---|---|---|---|
| 1,5 × 10³ | 5 | 0 | 95 | 4 | 0 | 96 |
| 2 × 10³ | 21 | 8 | 71 | 18 | 0 | 82 |
| 2,25 × 10³ | 49 | 5 | 46 | 41 | 0 | 59 |
| 2,50 × 10³ | 77 | 3 | 20 | 72 | 20 | 18 |
| 2,75 × 10³ | 89 | 6 | 5 | 89 | 1 | 10 |
| 3 × 10³ | 99 | 0 | 1 | 94 | 0 | 6 |
| 3,50 × 10³ | 100 | 0 | 0 | 99 | 0 | 1 |
| 4 × 10³ | 97 | 0 | 3 | 79 | 2 | 19 |
| 4,50 × 10³ | 86 | 4 | 10 | 70 | 14 | 16 |
| 5 × 10³ | 78 | 12 | 20 | 81 | 9 | 10 |

**Tabela 3:** Reconhecimento correto do motorista autorizado nº 3, sem e com óculos.

| Limiar | Sem óculos: CR | FR | NotR | Com óculos: CR | FR | NotR |
|---|---|---|---|---|---|---|
| 1,5 × 10³ | 10 | 13 | 7 | 8 | 0 | 92 |
| 2 × 10³ | 19 | 1 | 80 | 12 | 0 | 88 |
| 2,25 × 10³ | 20 | 9 | 71 | 18 | 3 | 79 |
| 2,50 × 10³ | 96 | 4 | 0 | 80 | 11 | 9 |
| 2,75 × 10³ **[N. T.: o original traz "2 × 753"]** | 80 | 13 | 7 | 79 | 1 | 20 |
| 3 × 10³ | 98 | 1 | 1 | 98 | 0 | 2 |
| 3,50 × 10³ | 99 | 1 | 0 | 97 | 1 | 2 |
| 4 × 10³ | 77 | 3 | 20 | 80 | 13 | 7 |
| 4,50 × 10³ | 86 | 9 | 5 | 75 | 15 | 10 |
| 5 × 10³ | 83 | 7 | 10 | 60 | 23 | 17 |

**Tabela 4:** Reconhecimento correto do motorista autorizado nº 4, sem e com óculos.

| Limiar | Sem óculos: CR | FR | NotR | Com óculos: CR | FR | NotR |
|---|---|---|---|---|---|---|
| 1,5 × 10³ | 86 | 2 | 12 | 72 | 0 | 28 |
| 2 × 10³ | 80 | 12 | 8 | 70 | 1 | 29 |
| 2,25 × 10³ | 87 | 3 | 10 | 75 | 13 | 12 |
| 2,50 × 10³ | 93 | 7 | 0 | 90 | 3 | 7 |
| 2,75 × 10³ | 95 | 2 | 3 | 93 | 2 | 5 |
| 3 × 10³ | 100 | 0 | 0 | 96 | 1 | 3 |
| 3,50 × 10³ | 99 | 1 | 0 | 82 | 8 | 10 |
| 4 × 10³ | 81 | 10 | 9 | 99 | 0 | 1 |
| 4,50 × 10³ | 66 | 20 | 14 | 60 | 3 | 37 |
| 5 × 10³ | 72 | 21 | 7 | 75 | 0 | 25 |

Os resultados da Tabela 5 mostram que o teste do sistema com o motorista autorizado nº 5 dá mais acurácia que os outros limiares quando o limiar vale 3 × 10³ e 3,50 × 10³, mesmo sem e com óculos.

**Tabela 5:** Reconhecimento correto do motorista autorizado nº 5, sem e com óculos.

| Limiar | Sem óculos: CR | FR | NotR | Com óculos: CR | FR | NotR |
|---|---|---|---|---|---|---|
| 1,5 × 10³ | 30 | 26 | 44 | 27 | 33 | 40 |
| 2 × 10³ | 69 | 20 | 11 | 60 | 28 | 12 |
| 2,25 × 10³ | 50 | 33 | 17 | 42 | 0 | 58 |
| 2,50 × 10³ | 93 | 4 | 3 | 90 | 0 | 10 |
| 2,75 × 10³ | 93 | 7 | 0 | 92 | 4 | 4 |
| 3 × 10³ | 99 | 0 | 1 | 98 | 0 | 2 |
| 3,50 × 10³ | 99 | 1 | 0 | 99 | 1 | 0 |
| 4 × 10³ | 67 | 13 | 20 | 65 | 5 | 30 |
| 4,50 × 10³ | 86 | 0 | 14 | 80 | 11 | 9 |
| 5 × 10³ | 87 | 0 | 13 | 8 | 5 | 15 |

**Tabela 6:** Reconhecimento correto no teste com motoristas não autorizados.

| Limiar | CR | FR | NotR |
|---|---|---|---|
| 1,5 × 10³ | 100 | 1 | 0 |
| 2 × 10³ | 100 | 0 | 0 |
| 2,25 × 10³ | 100 | 0 | 0 |
| 2,50 × 10³ | 100 | 0 | 0 |
| 2,75 × 10³ | 99 | 1 | 0 |
| 3 × 10³ | 100 | 0 | 0 |
| 3,50 × 10³ | 100 | 0 | 0 |
| 4 × 10³ | 100 | 0 | 0 |
| 4,50 × 10³ | 92 | 8 | 0 |
| 5 × 10³ | 87 | 13 | 0 |

**[N. T.: várias linhas das Tabelas 3, 5 e 6 não somam 100 (por exemplo, 10 + 13 + 7 = 30 na Tabela 3; 8 + 5 + 15 = 28 na Tabela 5; 100 + 1 + 0 = 101 na Tabela 6). Os valores foram mantidos como no original.]**

O resultado da Tabela 6 mostra que 100% dos motoristas não autorizados foram barrados pelo sistema proposto, especialmente com os limiares 3 × 10³ e 3,50 × 10³.

A Tabela 7 mostra o desempenho do sistema proposto em comparação com modelos comuns, aplicados às duas bases. A acurácia de reconhecimento com PCA isolada é de 87,9% na base ORL e de 95,2% na nossa base. Já com os algoritmos Fisher e ANN, o reconhecimento facial alcança 85,2% e 86,7%, respectivamente, na base ORL, e 96,2% e 96,8%, respectivamente, na nossa base. Os autores de [23] propuseram um sistema de reconhecimento com acurácia média de 74,4%, e os autores de [24] apresentam um sistema com acurácia média de 90,3% na base ORL. **[N. T.: a Tabela 7 traz 93,3% para [24].]** Por fim, o nosso sistema proposto, híbrido (Haar Cascade + PCA), alcança reconhecimento facial de 98,2% na base ORL e de 99,6% na nossa base.

A Tabela 8 compara a avaliação de desempenho entre o sistema proposto e os algoritmos existentes em termos de sensibilidade, precisão e especificidade, observando os valores de TP, TN, FN e FP nos experimentos com a nossa base. Fica claro que o sistema proposto funciona de forma extremamente eficaz e tem melhor desempenho.

**Tabela 7:** Comparação da acurácia média.

| Autor/técnica | Base ORL | Nossa base |
|---|---|---|
| PCA | 87,9% | 95,2% |
| Fisher | 85,2% | 96,2% |
| ANN | 86,7% | 96,8% |
| [23] | 74,4% | – |
| [24] | 93,3% | – |
| Proposto | 98,2% | 99,6% |

**Tabela 8:** Comparação de sensibilidade, precisão e especificidade.

| Autor/técnica | Sensibilidade | Precisão | Especificidade |
|---|---|---|---|
| PCA | 0,911 | 0,955 | 0,948 |
| Fisher | 0,899 | 0,942 | 0,881 |
| ANN | 0,906 | 0,916 | 0,935 |
| Proposto | 0,977 | 0,979 | 0,992 |

**Tabela 9:** Reconhecimento facial no computador × processador de baixo consumo (LPP).

| Autor/técnica | Tempo de reconhecimento no computador (s) | Tempo de reconhecimento no LPP (s) |
|---|---|---|
| PCA | 2,862 | 10,132 |
| Fisher | 2,997 | 23,279 |
| ANN | 2,942 | 19,680 |
| Proposto | 0,093 | 0,152 |

A Tabela 9 apresenta a comparação do tempo de reconhecimento (RT) entre o sistema proposto e outros algoritmos, implementados no computador e em processador de baixo consumo (LPP), respectivamente, usando a nossa base. Os resultados mostram que o tempo de execução do reconhecimento facial no computador não passou de 3 segundos. Já o tempo de execução desses métodos populares no processador de baixo consumo não foi adequado, por ser muito longo. Os resultados também mostraram que o sistema proposto levou menos tempo, sendo adequado para reconhecimento facial em processador de baixo consumo.

A Tabela 10 mostra o uso de CPU e de memória do reconhecimento facial com diferentes resoluções de câmera. Os resultados mostram que 640 × 480 deu melhor uso de memória e de CPU que as outras resoluções. **[N. T.: pela própria tabela, os menores valores são os de 160 × 120.]** O uso de CPU e de memória em percentual foi calculado pelas fórmulas 15 e 16, respectivamente:

**Tabela 10:** Uso de CPU e de memória do sistema proposto.

| Resolução da câmera | Uso de CPU (%) | Uso de memória (MB) |
|---|---|---|
| 1024 × 768 | 85 | 69,6 |
| 960 **[N. T.: assim no original]** | 80 | 64,9 |
| 640 × 480 | 81 | 60,1 |
| 320 × 240 | 84 | 55,2 |
| 160 × 120 | 76 | 53,5 |

$$U = \frac{R}{C} \times 100 \tag{15}$$

em que $U$ é a utilização; $R$ são os requisitos, isto é, o tempo de CPU ocupada; e $C$ é a capacidade, isto é, o tempo ocupado mais o tempo ocioso.

$$\text{Resultado} = \frac{\text{Memória física total} - (\text{Memória livre} + \text{Buffers} + \text{Cache})}{\text{Memória física total}} \times 100 \tag{16}$$

**[N. T.: a Equação 16 está quebrada no original; esta é a forma usual de calcular o percentual de memória usada, que parece ser a pretendida.]**

### 5.3 Análise de segurança

A segurança é uma questão importante para sistemas de segurança veicular. Esta subseção mostra a segurança do sistema proposto e de outra abordagem com base em alguns critérios. Os experimentos compararam o sistema proposto com o controlador de acesso AR-837E [25].

A Tabela 11 traz a comparação da taxa de reconhecimento, eficiência, segurança e preço. O sistema proposto foi melhor que o AR-837E. O AR-837E não tem capacidade de reconhecimento facial e tem segurança média em comparação com o nosso sistema. Além disso, por não usar cartão magnético, o nosso sistema não tem problema caso o cartão magnético seja roubado. Outro critério muito importante é o custo de implantação: o sistema proposto custa menos que o AR-837E.

**Tabela 11:** Comparação da análise de segurança.

| Critério | Sistema proposto | AR-837E [25] |
|---|---|---|
| Acurácia de identificação | Alta | Ausente |
| Eficiência | Alta | Alta |
| Segurança | Alta | Média |
| Preço | US$ 80 | US$ 200 |

## 6 Conclusões

Este artigo propôs um novo sistema inteligente de segurança veicular, chamado VSS-IoT, usando um chip de processamento de baixo consumo seguro, eficiente e de baixo custo, com a Internet como parte importante. Além disso, o artigo empregou mecanismos híbridos (Haar Cascade + PCA) para a detecção e o reconhecimento facial da imagem capturada por uma câmera USB. O classificador Haar cascade pode ser usado para rejeitar as regiões da imagem digital que provavelmente não contêm um rosto. Também é usado para detectar os rostos na imagem digital extraindo as melhores características. Já a PCA é um método matemático expresso como a transformação de imagens faciais de alta dimensão em poucas componentes principais, chamadas *eigenfaces*, usadas para reconhecer rostos na imagem digital. De acordo com os resultados experimentais iniciais, comparados com outros sistemas existentes, o VSS-IoT proposto alcançou a melhor taxa de acurácia, 98,2% na base ORL e 99,6% na nossa base, para identificar pessoas autorizadas e não autorizadas. O VSS-IoT também eleva a sensibilidade para 97,7%, o que é importante quando o sistema funciona sob diferentes condições de iluminação, quando o limiar vale 3 × 10³ e 3,50 × 10³. Além disso, o VSS-IoT melhorou o tempo em relação a outros sistemas, alcançando 0,152 s. Os resultados também mostraram que a resolução de câmera de 640 × 480 deu melhor uso de memória e de CPU que as outras, 76% e 53,5 MB respectivamente, o que é importante para sistemas de segurança veicular em tempo real. Portanto, pelo baixo custo e alto desempenho, o sistema é muito adequado para melhorar a segurança do setor automotivo.

**Agradecimentos:** os autores agradecem ao editor e aos revisores anônimos pelos valiosos comentários.

## Referências

As referências estão no idioma original.

[1] Mahesh R. P., Imdad R., "IoT Based Embedded System for Vehicle Security And Driver Surveillance", Proceedings of the 2nd International Conference on Inventive Communication and Computational Technologies (ICICCT 2018), IEEE.
[2] Vivek K. S., Soumitra M., Harshit M., "Car Security using Internet of Things", 1st IEEE International Conference on Power Electronics Intelligent Control and Energy Systems (ICPEICES-2016).
[3] Tabassum J. Kh., M. R. Bhadange, Pooja S. P., Vinaya S., "Smart Vehicle Monitoring System Using Raspberry Pi", Spvryan's International Journal of Engineering Sciences and Technology (SEST), 3(2), 2016.
[4] Liu Z., Zhang A., Li S., "Vehicle anti-theft tracking system based on Internet of things", IEEE International Conference on Vehicular Electronics and Safety (ICVES), Dongguan, 2013, pp. 48-52, doi: 10.1109/ICVES.2013.6619601.
[5] Arun Sasi, Lakshmi R. N., "Vehicle Anti-Theft System Based On An Embedded Platform", IJRET: International Journal of Research in Engineering and Technology, 2(9), 2013.
[6] Tahesin A., Prajakta Ch., Vidhi P., Megha G., Debajyoti M., "An Attempt to Develop an IoT based Vehicle Security System", 2018 IEEE International Symposium on Smart Electronic Systems (iSES), DOI 10.1109/iSES.2018.00050.
[7] Jian X., Haidong F., "A Low-cost Extendable Framework for Embedded Smart Car Security System", Proceedings of the 2009 IEEE International Conference on Networking, Sensing and Control, Okayama, Japan, 2009.
[8] Shruthi K., Ramaprasad P., Ray R., Naik M. A., Pansari S., "Design of anti-theft vehicle tracking system with a smartphone application", 2015 International Conference on Information Processing (ICIP), Pune, 2015, pp. 755-760, doi: 10.1109/INFOP.2015.7489483.
[9] Narayan T. D., Ravishankar S., "Face Detection and Recognition using Viola-Jones algorithm and fusion of LDA and ANN", IOSR Journal of Computer Engineering, 18(6), pp. 01-06, 2016.
[10] Kumar K. S., Shitala P., Vijay B. S., Tripathi R. C., "Real Time Face Recognition Using AdaBoost Improved Fast PCA Algorithm", International Journal of Artificial Intelligence and Applications (IJAIA), 2(3), 2011.
[11] Shaik M. A. et al., "An Inexpensive Security Authentication System Based on a Novel Face-Recognition Structure", International Journal of Engineering Trends and Technology (IJETT), 4(9), 2013.
[12] Mohammad D., Amin A., Olivier D., "Face Detection using Viola and Jones Method and Neural Networks", International Conference on Information and Communication Technology Research (ICTRC2015), pp. 40-43, IEEE, 2015.
[13] Ahmed A. E., "IoT-based Efficient Tamper Detection Mechanism for Healthcare Application", International Journal of Network Security, 20(3), pp. 489-495, 2018, DOI: 10.6633/IJNS.201805.20(3).11.
[14] Siddarth R., Dattatreya P., Sadique N., "Face recognition using PCA and LDA: Analysis and comparison", IEEE International Conference on Advances in Recent Technology in Communication and Computing, pp. 6-16, 2013.
[15] Varsha G., Dipesh Sh., "A study of various Face Detection Methods", International Journal of Advanced Research in Computer and Communication Engineering, 3(5), 2014.
[16] Bavya R., Mohanamurali R., "Next generation auto theft prevention and tracking system for land vehicles", International Conference on Information Communication and Embedded Systems (ICICES), Chennai, 2014, pp. 1-5, doi: 10.1109/ICICES.2014.7033987.
[17] Zhixiong L., Guiming H., "A Vehicle Anti-theft and Alarm System Based on Computer Vision", IEEE International Conference on Vehicular Electronics and Safety, 2005, DOI: 10.1109/ICVES.2005.1563666.
[18] Sarvesh V. A., Chetana R., "Face Recognition System for Unlocking Automobiles Using GSM and Embedded Technology", International Journal of Advanced Research in Electrical, Electronics and Instrumentation Engineering, 5(7), 2016.
[19] Christina Ma., Fernandez D., Kristina J. E. G., Aubrey R. M. L., Ron J. J. R., Argel A. B., Elmer P. D., "Simultaneous Face Detection and Recognition using Viola-Jones Algorithm and Artificial Neural Networks for Identity Verification", 2014 IEEE Region 10 Symposium, pp. 672-676, 2014.
[20] Viola P., Jones M., "Rapid Object Detection using a Boosted Cascade of Simple Features", Conference on Computer Vision and Pattern Recognition, 2001.
[21] Turk M. A., Pentland A. P., "Eigenfaces for Recognition", Journal of Cognitive Neuroscience, 3(1), pp. 71-86, 1991.
[22] The ORL face database: http://www.cl.cam.ac.uk/Research/DTG/attarchive/facedatabase.html.
[23] Ebrahimpour R., Nazari M., Azizi M., Amiri A., "Single Training Sample Face Recognition Using Fusion of Classifiers", International Journal of Hybrid Information Technology, 4(1), 2011.
[24] Novosel R., Meden B., Emersic Z., Struc V., Peer P., "Face recognition with Raspberry Pi for IoT Environments", International Electrotechnical and Computer Science Conference ERK 2017, Portorož, Slovenia, 2017.
[25] AR-837E Access card reader, http://www.soga.com.tw/content/product/180/index.html.

---

## Notas para o TCC

*Seção acrescentada nesta tradução; não faz parte do artigo original.*

- **Por que importa:** é um sistema IoT com Raspberry Pi que identifica pessoas por rosto dentro de um veículo e avisa remotamente, uma arquitetura próxima da do projeto.
- **Cuidado com os números:** 98,2% (ORL) e 99,6% vêm de bases pequenas e controladas: 40 pessoas na ORL e 50 motoristas, com 10 fotos de treino cada, na base própria. O limiar foi escolhido olhando os mesmos dados de teste, e há tabelas com linhas que não somam 100. Use como exemplo de arquitetura, não como prova de que PCA rivaliza com redes profundas. Isso já está registrado no item E3 do [documento de lacunas](../lacunas_revisao_bibliografica.md).
- **Contraste com o projeto:** o artigo envia a foto do intruso por e-mail e pelo Firebase. O TCC faz o contrário, por causa da LGPD: nenhuma imagem sai do dispositivo (RF-05).
- **Ponto útil:** a Tabela 9 mostra que o mesmo algoritmo fica de 3 a 8 vezes mais lento na Raspberry Pi do que no PC, o que reforça a ressalva de medir o tempo no hardware final (item M4 do documento de lacunas).
