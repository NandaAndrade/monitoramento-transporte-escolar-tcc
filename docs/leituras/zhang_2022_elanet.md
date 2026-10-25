# Rede de atenção leve e eficiente para reconhecimento facial (ELANet)

> **Tradução integral para o português**, feita para estudo do TCC.
>
> **Original:** ZHANG, P.; ZHAO, F.; LIU, P.; LI, M. Efficient Lightweight Attention Network for Face Recognition. *IEEE Access*, v. 10, p. 31740–31750, 2022. DOI: [10.1109/ACCESS.2022.3150862](https://doi.org/10.1109/ACCESS.2022.3150862).
>
> **Licença:** o original é publicado em acesso aberto sob a licença [Creative Commons Atribuição 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br). Esta tradução é uma obra derivada: o texto foi traduzido do inglês, as figuras foram substituídas por suas legendas e foram acrescentadas notas da tradução, marcadas como **[N. T.]**, e a seção final "Notas para o TCC". Os autores originais não revisaram nem endossam esta tradução.
>
> **Limitação desta tradução:** as Tabelas 1 a 8 do original são imagens e não puderam ser extraídas do PDF. O texto que as comenta foi traduzido, mas os valores das tabelas precisam ser consultados no PDF.
>
> **PDF local:** `Downloads/Referencias/zhang_2022_elanet.pdf`

---

**Peng Zhang, Feng Zhao, Peng Liu e Mengwei Li**
Escola de Instrumentação e Eletrônica e Escola de Engenharia Elétrica e de Controle, North University of China, Taiyuan, China.
Recebido em 24 jan. 2022; aceito em 7 fev. 2022; publicado em 10 fev. 2022.
Trabalho financiado pelo General Area Fund, projeto 6140003050110.

## Resumo

Embora o reconhecimento facial tenha alcançado grande sucesso graças ao aprendizado profundo, muitos fatores podem afetar a qualidade dos rostos em condições não controladas, como mudanças de pose, variações de idade e mudanças de luz, o que pode prejudicar seriamente o desempenho do reconhecimento. Neste trabalho, propõe-se uma abordagem eficaz chamada Redes de Atenção Leves e Eficientes (ELANet) para enfrentar o desafio do impacto da pose e da idade no desempenho do reconhecimento facial. Primeiro, regiões locais semelhantes do rosto são particularmente importantes quando a geometria e a aparência do rosto mudam drasticamente. Para amenizar esse desafio, a atenção espacial é usada para captar regiões locais semelhantes importantes, e a atenção de canal é empregada para focar em características com diferentes níveis de importância. Além disso, o módulo de Atenção de Fusão Eficiente (EFA) é projetado para obter melhor desempenho, reduzindo o esforço computacional necessário para fundir a atenção espacial e a de canal. Segundo, o aprendizado de características em múltiplas escalas é necessário, porque mudanças de pose ou de expressão grandes podem fazer regiões de reconhecimento semelhantes aparecerem em escalas diferentes. Para isso, apresenta-se um módulo piramidal de múltiplas escalas, que constrói uma série de características em escalas diferentes por meio de operações de *pooling*. Terceiro, para unir a informação de detalhe local de baixo nível com a informação semântica de alto nível, as características de camadas diferentes são fundidas pela Fusão Espacial Adaptativa de Características (ASFF), em vez de simplesmente somadas ou concatenadas. Em comparação com redes leves recentes, a ELANet melhorou o desempenho em 1,83% e 2,17% nas bases CPLFW e VGG2_FP, respectivamente, e em 0,92% na base CALFW. A ELANet enfrenta o desafio do impacto da pose e da idade no reconhecimento facial com poucos parâmetros e pouco esforço computacional, sendo adequada para dispositivos embarcados e móveis.

**Termos indexadores:** reconhecimento facial, características locais, múltiplas escalas, rede leve.

## I. Introdução

Avanços significativos foram alcançados no reconhecimento facial com o uso de redes neurais convolucionais profundas (DCNNs) [1], [2], [3]. No entanto, a maioria dos trabalhos não considera ao mesmo tempo a importância das características hierárquicas em múltiplas escalas e das regiões locais para o reconhecimento facial.

Muitos fatores influenciam o desempenho do reconhecimento facial, como postura, idade, iluminação, oclusão ou variações de qualidade. Por exemplo, como mostra a Figura 1, as imagens de rosto da segunda linha estão sujeitas a diferentes fatores não controlados, que ainda são um desafio para os algoritmos atuais de reconhecimento facial, embora possam ser reconhecidas facilmente por humanos. E esses problemas podem levar a grandes mudanças na geometria e na aparência do rosto. Em contraste, as áreas locais semelhantes do rosto são particularmente importantes. Vários trabalhos dependem de pontos de referência faciais (*landmarks*) para obter informação local do rosto [4], [5]. Porém, a detecção de pontos de referência pode falhar por causa de variações de postura, idade, iluminação, oclusão ou qualidade.

> [Figura 1: Os rostos são afetados por vários fatores não controlados, como postura, idade, iluminação, oclusão ou variações de qualidade.]

Como ilustra a Figura 1, mudanças de pose fazem partes do rosto desaparecerem; imagens borradas deixam toda a área do rosto pouco nítida; mudanças de iluminação fazem perder informações de detalhe do rosto. Regiões diferentes do rosto podem contribuir em graus diferentes para o resultado final do reconhecimento. A atenção espacial é incorporada para caracterizar automaticamente as regiões informativas e extrair informação local. Conforme apresentado em [6], a Rede de Agregação Local (LANet) é usada para localizar os domínios mais distinguíveis do rosto e obtém bom desempenho em bases relacionadas a postura e idade. Além disso, a atenção de canal busca destacar canais importantes e suprimir canais com menos informação. Os canais de características de baixo nível contêm informação de detalhes locais, e os canais de alto nível representam informação semântica de alto nível. Assim, a Rede de Compressão e Excitação (SENet) [7] recalibra de forma adaptativa a resposta das características de cada canal, modelando as interdependências entre os canais, e traz melhorias significativas de desempenho aos modelos de CNN com um pequeno aumento do custo computacional. Ao usar CNNs para extrair características do rosto, as regiões mais reconhecíveis do rosto devem receber mais peso e, da mesma forma, os canais com a informação mais distintiva devem receber mais peso. É intuitivo combinar as duas coisas para obter melhor desempenho. Ao mesmo tempo, para aliviar o esforço computacional causado por essa fusão, o módulo de Atenção de Fusão Eficiente (EFA) é introduzido no nosso modelo.

Representar características em múltiplas escalas é útil em várias tarefas de visão [6], [8], [9]. Características em múltiplas escalas são necessárias no reconhecimento facial porque regiões locais do rosto podem ter tamanhos ou formas variados por causa de mudanças faciais drásticas. Como mostram a terceira e a quarta linhas da Figura 1, as bocas têm tamanhos variados nas colunas 1, 2, 3 e 6; os olhos aparecem em tamanhos diferentes nas colunas 3, 4 e 5. A maioria dos métodos não considera que a informação útil nem sempre está fixa na mesma camada. O trabalho [8] extrai características em múltiplas escalas com uma rede de atenção diversa baseada em pirâmide hierárquica para enfrentar esse desafio e usa aprendizado diverso para amenizar o problema de respostas redundantes. Esse método também alcança resultados de ponta nos desafios de postura e idade. No entanto, regiões locais discriminativas do rosto podem aparecer em camadas diferentes. Por isso, propõe-se um módulo piramidal de múltiplas escalas, capaz de redimensionar características da mesma camada para tamanhos diferentes, a fim de extrair mais características locais.

As características de alto nível têm campos receptivos maiores e representam informação semântica de alto nível. Por isso, a maioria dos trabalhos anteriores não usa as características de baixo nível com informação local, mas usa diretamente a última camada de convolução. Essas abordagens inevitavelmente perdem detalhes locais ou informação de baixo nível e pequena escala. Para amenizar esses problemas, [10] obtém as características locais da primeira camada da rede e as globais por análise de componentes principais. Em comparação com a MobileNet [11], esse método extrai uma informação de características mais completa. O trabalho [12] combina informação de características de baixo e de alto nível para obter representações diferentes. No entanto, todos esses métodos usam soma ou concatenação simples.

Este artigo propõe as Redes de Atenção Leves e Eficientes (ELANet), adequadas para reconhecimento facial em dispositivos móveis ou embarcados. As contribuições do artigo são as seguintes:

1. A ELANet proposta pode aprender características em múltiplas escalas a partir da mesma camada e características locais a partir de camadas diferentes. O módulo piramidal de múltiplas escalas proposto é incorporado à ELANet. Esse módulo incentiva o modelo a aprender características em múltiplas escalas, dividindo a mesma característica em características de escalas diferentes por meio de operações de *pooling*. A ELANet tem poucos parâmetros e poucos cálculos, sendo muito adequada para implantação em dispositivos móveis ou embarcados.
2. A atenção espacial e a de canal são introduzidas simultaneamente no módulo EFA. Um módulo SENet é usado para atribuir pesos diferentes a canais diferentes de acordo com sua importância, destacando os canais discriminativos e suprimindo os de menos informação. O módulo LANet localiza as regiões mais discriminativas do rosto. O módulo EFA obtém melhor desempenho, reduzindo o esforço computacional da fusão, e permite focar nas características locais.
3. Para unir a informação de detalhe local de baixo nível com a informação semântica de alto nível, as características de camadas diferentes são fundidas por Fusão Espacial Adaptativa de Características (ASFF), em vez de simples soma ou concatenação. A abordagem proposta funde características hierárquicas para obter informação de características mais completa.

O restante do artigo está organizado assim: a Seção II revisa brevemente os trabalhos sobre reconhecimento facial e mecanismos de atenção. A Seção III descreve a ELANet em detalhe; a Seção IV apresenta os resultados dos experimentos e discute em detalhe o desempenho da ELANet. A Seção V traz as conclusões e discute trabalhos futuros.

## II. Trabalhos relacionados

Apresenta-se uma breve revisão sobre reconhecimento facial e mecanismos de atenção.

### A. Reconhecimento facial

As DCNNs alcançaram grande sucesso no reconhecimento facial. Pela simplicidade e pela interpretabilidade probabilística, a função de perda *softmax* é considerada um dos componentes importantes das CNNs. Assim, no início, as abordagens de reconhecimento facial usavam principalmente a perda *softmax*, mas ela não consegue reduzir de forma eficaz a variância intraclasse nem aumentar a variância interclasse. Várias funções de perda novas foram propostas em [1], [3] para reduzir ainda mais a variância intraclasse e aumentar a interclasse. No entanto, a maioria delas não leva em conta, de forma eficaz, as representações em múltiplas escalas e as características locais do rosto.

#### 1) Reconhecimento facial em múltiplas escalas

A representação de características em múltiplas escalas é de grande importância para o reconhecimento facial. O trabalho [6] aprende representações em múltiplas escalas sob duas perspectivas: por um lado, usa núcleos de convolução de tamanhos diferentes para extrair informação de múltiplas escalas na mesma camada; por outro, conecta a saída de cada camada para aprender características em múltiplas escalas entre camadas. O trabalho [9] substitui um conjunto de filtros 3 × 3 por um conjunto de filtros menores, conectando os diferentes grupos de filtros em um estilo hierárquico semelhante ao residual. O trabalho [13] usa estruturas diferentes de CNN no mesmo nível para extrair características em múltiplas escalas. No entanto, a maioria não percebe que as características podem cobrir uma faixa maior de escalas dentro de uma mesma camada. Assim, o módulo piramidal de múltiplas escalas proposto divide a mesma característica em características de escalas diferentes por meio de operações de *pooling*.

#### 2) Representações de características locais

O aprendizado de representações locais pode lidar de forma eficaz com variações de postura e de idade. O trabalho [4] treina várias CNNs em regiões do rosto, mas as características gerais do rosto são ignoradas. O trabalho [5] une características de várias regiões do rosto com características globais, compartilhando características rasas e intermediárias. O trabalho [14] trata a variação de pose aprendendo simultaneamente o alinhamento e a extração de características, por meio de convolução deformável com campos de deslocamento espacial. A maioria dos métodos depende inevitavelmente de pontos de referência faciais. Porém, a detecção desses pontos pode falhar por causa de variações de postura, idade, iluminação, oclusão ou qualidade.

### B. Mecanismos de atenção

Uma tendência tem sido a investigação da atenção. Os mecanismos de atenção têm papel muito importante na visão computacional [7], [15], [16]. A atenção atribui mais peso às características mais informativas e suprime as menos úteis. No entanto, poucos estudos aplicaram atenção à tarefa geral de reconhecimento facial. Atenção residual e autoatenção foram combinadas para tratar o reconhecimento facial entre idades em [17]. Uma atenção eficiente foi introduzida para reconhecer rostos em várias poses em [18]. Dois blocos de atenção foram usados para agregar de forma adaptativa vetores de características em uma única característica, para reconhecimento facial em vídeo, em [19]. Um módulo SENet aprimorado foi aplicado em [20], e a autoatenção é usada para captar informações mais detalhadas [21]. A LANet e a SENet foram introduzidas em sequência para localizar automaticamente a região mais distintiva do rosto em [6]. No entanto, a maioria dessas abordagens aplica apenas implementações isoladas de atenção, ou aplica as atenções em sequência. Neste trabalho, para obter melhor desempenho, a atenção de canal e a espacial são fundidas. Além disso, o EFA proposto é usado para aliviar a sobrecarga computacional causada pela fusão.

## III. Uma nova rede

O modelo ELANet proposto contém principalmente três módulos: o módulo de gargalo com atenção, o módulo piramidal de múltiplas escalas e o módulo ASFF.

### A. Gargalo com atenção (*bottleneck-attention*)

A MobileNet [22], [11] constrói redes leves por meio de convolução separável em profundidade (*depthwise separable*) e de uma estrutura residual invertida: a convolução separável em profundidade reduz o número de parâmetros necessários, e a estrutura residual invertida garante o desempenho do modelo. O núcleo da MobileNet é o gargalo (*bottleneck*). Assim, combinar o EFA com o gargalo resulta no BA, como mostra a Figura 2. **[N. T.: o original diz "Fig. 1", mas o bloco BA está na Figura 2.]**

> [Figura 2: Estrutura do bloco BA, em que h é a altura da característica, ω é a largura e c é o número de canais; c′ = t · c, h′ = h/S e ω′ = ω/S, em que S é o passo (*stride*) e t é o fator de expansão.]

O módulo BA consiste principalmente em dois núcleos de convolução 1 × 1, um núcleo de convolução separável em profundidade 3 × 3 e um módulo EFA, que executam operações diferentes com vários tamanhos de passo. O primeiro módulo de convolução 1 × 1 expande os canais de características para extrair mais informação; o segundo é introduzido para reduzir os canais; o módulo de convolução separável em profundidade 3 × 3 é usado para reduzir a quantidade de parâmetros. Para evitar que a unidade linear retificada (ReLU) destrua características, usa-se uma ativação linear na parte final da saída. Além disso, para casar as dimensões do atalho (*shortcut*), propõem-se duas estruturas diferentes para o módulo BA. Quando o passo é 1, o atalho é usado para melhorar o desempenho do modelo, como na estrutura residual; um módulo de convolução com passo 2 é usado para subamostragem.

### B. Módulo EFA

Para obter melhor desempenho, propõe-se o módulo EFA, que funde a SENet e a LANet em vez de usá-las separadamente, como mostra a Figura 3. O módulo EFA pode aliviar o esforço computacional necessário para fundir as atenções espacial e de canal.

> [Figura 3: Estrutura do módulo EFA, em que h é a altura da característica, ω é a largura, c é o número de canais e g é o número de grupos.]

Seja a característica $X \in \mathbb{R}^{h \times \omega \times c}$ a entrada do módulo EFA, em que $h$, $\omega$ e $c$ representam a altura, a largura e o número de canais, respectivamente. Primeiro, as características de entrada são divididas em saídas de grupos diferentes $[X_1, X_2, \cdots, X_g]$, em que $g$ é o número de grupos. $X_i \in \mathbb{R}^{h \times \omega \times c_i}$ é a saída do $i$-ésimo grupo, em que $c_i$ representa o número de canais. O número de canais de cada camada de saída é determinado por $c$ e $g$.

Segundo, o $i$-ésimo grupo é dividido em dois grupos de igual número de canais, $[X_{i1}, X_{i2}]$. Para reter informação espacial e de canal, são usados o módulo LANet [6] e o módulo SENet [7].

A LANet, mostrada na Figura 4, usa duas camadas consecutivas de convolução 1 × 1. A primeira camada convolucional produz $c/r$ canais, em que $c$ é o número de canais de entrada e $r$ é a taxa de redução, seguida de uma função ReLU. Em seguida, uma característica de saída com 1 dimensão é gerada por uma camada de convolução 1 × 1 seguida de uma função sigmoide; essa saída é chamada de atenção espacial. Por fim, a saída da LANet é a característica de entrada ponderada pela atenção espacial.

> [Figura 4: Estrutura do módulo LANet, em que h, ω, c e r representam a altura, a largura, o número de canais e a taxa de redução, respectivamente.]

A estrutura da SENet aparece na Figura 5. Para obter um descritor único, a operação de compressão (*squeeze*) condensa a informação global de cada canal por *pooling* de média global. Formalmente, a estatística $z \in \mathbb{R}^c$ é obtida para o canal $t$ reduzindo $U$ ao longo das dimensões espaciais da característica:

$$z_t = F_{sq}(u_c) = \frac{1}{H \times W}\sum_{i=1}^{H}\sum_{j=1}^{W} u_c(i, j) \tag{1}$$

em que $u(i, j)$ é o elemento na posição $(i, j)$ do canal $t$ e $H \times W$ é a dimensão espacial. A operação de excitação aprende os coeficientes de peso de cada canal, tornando o modelo mais discriminativo em relação às características de cada canal. São usadas duas camadas totalmente conectadas (FC), uma de redução de dimensão, $\omega_1$, e uma de expansão de dimensão, $\omega_2$:

$$s = F_{ex}(z, w) = \sigma\left(\omega_2\, \delta(\omega_1 z)\right) \tag{2}$$

em que $\sigma$ é a função sigmoide e $\delta$ é a função ReLU. A camada de redução produz $c/r$ canais, e a de expansão produz $c$ canais. Por fim, os valores de ativação aprendidos para cada canal são multiplicados pelas características de entrada. Por concatenação, a saída final $j$, com $j \in [1, 2, \cdots, g]$, tem o mesmo número de canais que o $i$-ésimo grupo.

> [Figura 5: Estrutura do módulo SENet, em que h é a altura da característica, ω é a largura e c é o número de canais; $F_{sq}(\cdot)$ é a operação de compressão e $F_{ex}(\cdot)$ é a operação de excitação.]

Por fim, os $g$ grupos de subcaracterísticas, $i \in [1, 2, \cdots, g]$, são agregados e depois passados pelo operador de "embaralhamento de canais" (*channel shuffle*) [23].

### C. Módulo piramidal de múltiplas escalas

A estrutura aparece na Figura 6. As características de uma mesma camada passam a ter representações locais em múltiplas escalas, para extrair características mais finas.

> [Figura 6: A estrutura do módulo piramidal de múltiplas escalas consiste em quatro partes: o módulo EFA, o módulo de sobreamostragem, o módulo de produto e o módulo de concatenação.]

Dado um mapa de características $X \in \mathbb{R}^{h \times \omega \times c}$, em que $h$, $\omega$ e $c$ representam a altura, a largura e o número de canais, o módulo piramidal de múltiplas escalas primeiro divide a característica $X$ em saídas de tamanhos diferentes por meio de operações de *pooling*:

$$X = [X_1, X_2, \cdots, X_s], \quad X_i \in \mathbb{R}^{h_i \times \omega_i \times c} \tag{3}$$

em que $h_i \times \omega_i$ é o tamanho da subcaracterística. O maior tamanho de subcaracterística é igual ao da característica de entrada. Segundo, a informação espacial e de canal de cada subcaracterística $X_i$ é obtida pelo módulo EFA, seguido de uma convolução 1 × 1. As características de cada escala são sobreamostradas por interpolação bilinear, e as características sobreamostradas são definidas como $X_{ij}$, com $i = j \in [1, 2, \cdots, s]$, do mesmo tamanho da entrada. Em seguida, os mapas de características refinados $R_{ij}$, com $i = j \in [1, 2, \cdots, s]$, são obtidos pelo produto de $X_{ij}$ com a entrada $X$:

$$R_{ij} = X_{ij} \circ X \tag{4}$$

em que $\circ$ denota o produto de Hadamard (elemento a elemento). Por fim, para produzir o mesmo número de canais da entrada, os mapas refinados são ligados por um módulo de concatenação, seguido de uma convolução 1 × 1.

### D. ASFF

A maioria dos trabalhos anteriores não usa as características de baixo nível com informação local, mas usa diretamente a última camada convolucional para aprender as características. Essas abordagens não consideram que a representação obtida em cada camada não é completa. Assim, é natural integrar as características das diferentes camadas.

O módulo piramidal de múltiplas escalas é aplicado a cada dois módulos BA. Assim, ele extrai, com o módulo EFA, características mais integradas de camadas diferentes. Diferentemente dos métodos anteriores, que agregam a informação de camadas diferentes por soma elemento a elemento ou concatenação, adota-se a abordagem de [24] para integrar a informação de vários níveis, em duas etapas: transformação de escala e fusão adaptativa.

Define-se $x^l$ como as características no nível $l$. A característica $x^{n \to l}$ ($n \neq l$) denota o redimensionamento das características do nível $n$ para o nível $l$. Na rede, as características de camadas diferentes têm escalas e números de canais variados. Por isso, adotam-se estratégias diferentes de sobreamostragem e de subamostragem para as diferentes escalas. Na sobreamostragem, uma convolução 1 × 1 ajusta o número de canais, seguida de interpolação bilinear para aumentar a resolução. Na subamostragem pela metade, usa-se uma convolução 2 × 2 com passo 2 e preenchimento 1, para mudar ao mesmo tempo o número de canais e a resolução. Para a razão de 1/4, acrescenta-se um *max-pooling* com passo 2 antes da convolução.

A característica na posição $(i, j)$ do mapa é indicada por $x_{ij}^{n \to l}$. As camadas interagem entre si para obter uma informação mais completa:

$$y_{ij}^l = \alpha_{ij}^l \cdot x_{ij}^{1 \to l} + \beta_{ij}^l \cdot x_{ij}^{2 \to l} + \gamma_{ij}^l \cdot x_{ij}^{3 \to l} \tag{5}$$

em que $y_{ij}^l$ é o vetor $(i, j)$ dos mapas de saída $y^l$ ao longo dos canais. $\alpha_{ij}^l$, $\beta_{ij}^l$ e $\gamma_{ij}^l$ são os pesos espaciais dos diferentes níveis em relação ao nível $l$, aprendidos de forma adaptativa pela rede. $\alpha_{ij}^l$ é calculado pela fórmula:

$$\alpha_{ij}^l = \frac{e^{\lambda_{\alpha_{ij}}^l}}{e^{\lambda_{\alpha_{ij}}^l} + e^{\lambda_{\beta_{ij}}^l} + e^{\lambda_{\gamma_{ij}}^l}} \tag{6}$$

em que $\lambda_{\alpha_{ij}}^l$, $\lambda_{\beta_{ij}}^l$ e $\lambda_{\gamma_{ij}}^l$ são os parâmetros de controle da função *softmax*, que força $\alpha_{ij}^l + \beta_{ij}^l + \gamma_{ij}^l = 1$, com $\alpha_{ij}^l, \beta_{ij}^l, \gamma_{ij}^l \in [0, 1]$.

Por fim, uma camada FC reduz a dimensão de saída para 128.

### E. Redes de atenção leves e eficientes

Pelo desempenho superior e pelo uso de menos parâmetros que as redes leves populares, usa-se a MobileFaceNet [2] como base. O módulo EFA é introduzido em um gargalo, como mostra a Figura 2, formando o BA. A SENet e a LANet são combinadas no módulo EFA, como ilustra a Figura 3, sendo aplicadas simultaneamente. Características em múltiplas escalas são necessárias para o reconhecimento facial, porque regiões locais do rosto podem ter tamanhos ou formas variados por causa de mudanças faciais drásticas. Ao mesmo tempo, regiões locais discriminativas podem aparecer em camadas diferentes, e as características podem cobrir uma ampla faixa de escalas em uma mesma camada convolucional. Para resolver esses problemas, o módulo piramidal de múltiplas escalas é introduzido com o módulo EFA, como mostra a Figura 6. Os módulos piramidais são aplicados a cada dois módulos BA, para extrair características mais integradas de camadas diferentes. A maioria dos métodos usa apenas a última camada convolucional e inevitavelmente perde detalhes locais ou informação de baixo nível e pequena escala. Além disso, métodos de fusão simples dão resultados abaixo do ótimo. Como a ASFF funde as características de forma adaptativa e tem custo quase nulo, ela é usada para agregar as características ricas das diferentes camadas. Assim, propõe-se um novo modelo, a ELANet, para dispositivos móveis ou embarcados. Ela aprende características em múltiplas escalas e características locais, e as funde com as globais para aumentar a expressividade do modelo.

A estrutura geral do modelo ELANet aparece na Figura 7. Ela inclui quatro partes: entradas, características locais, características globais e saídas. A camada de convolução inclui duas operações: uma convolução 3 × 3 e uma convolução separável em profundidade 3 × 3. O módulo BA proposto é repetido $n$ vezes, como mostra a Figura 2, e descreve as características locais importantes e a importância dos canais. O módulo piramidal de múltiplas escalas e a ASFF aprendem características locais em múltiplas escalas e as fundem entre camadas. As características locais e globais são fundidas, e características de 128 dimensões saem pela camada totalmente conectada. Como função de perda, usa-se a ArcFace [3], para reduzir a variância intraclasse e ampliar a interclasse, segundo a formulação:

$$L = -\frac{1}{N}\sum_{i=1}^{N} \log \frac{e^{s\cos(\theta_{y_i} + m)}}{e^{s\cos(\theta_{y_i} + m)} + \sum_{j=1, j \neq y_i}^{n} e^{s \cos\theta_j}} \tag{7}$$

em que $N$ é o tamanho do lote, $n$ é o número de classes, $s$ é o raio da hiperesfera da distribuição das características, $m$ é a margem angular aditiva e $\theta_j$ é o ângulo entre o peso $W_j$ e a característica $x_i$.

> [Figura 7: Estrutura da ELANet proposta.]

## IV. Resultados experimentais e discussão

São apresentados os resultados experimentais da ELANet. As bases de treino e de teste são explicadas e os experimentos de ablação são demonstrados. Em seguida, a ELANet é comparada com outras redes populares. São mostrados experimentos entre poses e entre idades. Por fim, o desempenho do modelo é avaliado nas bases IJB-B/C e comparado com métodos de ponta.

### A. Dados de treino e de teste

#### 1) Bases de treino

As bases MS1MV3 [25] e VGGFace2 [26] são usadas para o treino.

- **MS1MV3:** também chamada de MS1M-RetinaFace, é a base MS1MV0 [27] limpa por um método semiautomático. Contém 5,1 milhões de imagens de rosto de 93 mil identidades.
- **VGGFace2:** contém 3,14 milhões de imagens de rosto, com grande variedade de poses, idades e etnias. Quando não for indicado o contrário, a MS1MV3 é a base de treino.

#### 2) Bases de teste

São usadas para teste as bases LFW [28], CALFW [29], CPLFW [30], CFP [31], VGGFace2-FP [26] e IJB-B/C [32].

- **LFW:** contém 13.233 imagens de 5.749 pessoas famosas, com fundos, orientações e expressões faciais diferentes, e é a referência para reconhecimento facial não controlado. Para a validação cruzada, são propostos pares de imagens divididos em 10 partes.
- **Entre poses:** a base CFP tem 500 pessoas, com 10 rostos frontais e 4 de perfil de cada uma. A base é dividida em 10 partes, com conjuntos de pessoas disjuntos em cada protocolo. A base CPLFW tem 3.000 pares positivos com poses amplas, para aumentar a influência da pose no reconhecimento facial. A base contém apenas pares negativos de mesma raça e gênero, para reduzir o efeito de diferenças de atributos, com 2 ou 3 imagens por pessoa. A base VGGFace2-FP contém 3,14 milhões de imagens de 8.631 pessoas, cobrindo ampla faixa de poses, idades e etnias.
- **CALFW:** tem 4.025 pessoas, com 2, 3 ou 4 imagens cada. Para aumentar a variância intraclasse causada pelo envelhecimento, contém muitas imagens de rosto em idades variadas, e apenas pares negativos de mesma raça e gênero, para reduzir o efeito de diferenças de atributos.
- **Entre qualidades:** a base IJB-B contém 11.754 imagens de rosto de 1.845 pessoas, 55.026 quadros de vídeo, 7.011 vídeos e 10.044 imagens sem rosto. A base IJB-C contém 21.294 imagens de rosto de 3.531 pessoas e 10.040 imagens sem rosto.

### B. Detalhes de implementação

A ELANet foi implementada em PyTorch [33]. O hiperparâmetro $s$ é 64 e a margem angular $m$ da ArcFace é 0,5, segundo [34]. O tamanho do lote é 256, e uma GPU NVIDIA 3090 (24 GB) é usada no treino. A taxa de aprendizado inicial é 0,1, dividida por 10 a cada época. O treino termina após 25 épocas. O momento é 0,9 e o decaimento dos pesos é 5 × 10⁻⁴.

### C. Estudo de ablação

Primeiro, esta seção demonstra a importância dos três componentes: módulo BA, módulo piramidal de múltiplas escalas e ASFF. Compara-se o desempenho de diferentes combinações de LANet e SENet. Depois, investiga-se o efeito do hiperparâmetro de redução $r$ e do número de grupos $g$ no desempenho do modelo. Por fim, mostra-se o desempenho dos diferentes métodos de fusão.

> [Tabela 1: Comparação de desempenho entre modelos diferentes em bases diferentes, com taxa de redução r = 2 e número de grupos g = 2. Valores no PDF original.]

> [Tabela 2: Comparação de desempenho entre modelos diferentes em bases diferentes, com taxa de redução r = 2 no módulo EFA e número de grupos g = 2. Valores no PDF original.]

#### 1) A importância dos três módulos

Para entender melhor o modelo ELANet, analisam-se os módulos: o gargalo [1], o módulo BA, o módulo piramidal de múltiplas escalas e o módulo ASFF. A importância de cada módulo é estudada na Tabela 1.

O desempenho do módulo BA melhora significativamente em relação ao modelo original. Isso ocorre porque o módulo EFA é acrescentado ao modelo original, permitindo destacar tanto onde estão as partes do rosto quanto quais características são significativas. Os resultados da Tabela 1 mostram que o aprendizado piramidal de características em múltiplas escalas e a fusão de informação entre camadas são necessários. Como ilustra a Tabela 1, a ELANet proposta tem melhor desempenho. O modelo ELANet supera todas essas variantes em dois aspectos. Por um lado, incorpora o módulo piramidal de múltiplas escalas para extrair características em múltiplas escalas e enriquecer a informação fina das características. Por outro, usa a ASFF para fundir informações de níveis diferentes, o que torna a informação final mais completa e rica e ajuda a melhorar a acurácia do reconhecimento.

#### 2) Diferentes combinações de atenção

Esta seção examina o efeito de diferentes combinações de SENet e LANet no desempenho do modelo. São mostradas quatro combinações: a primeira usa apenas o módulo SENet; a segunda, apenas o módulo LANet; a terceira usa a atenção dupla de rosto (DFA) [6]; e a última é o módulo EFA.

A Tabela 2 resume os resultados. A LANet destaca onde estão as partes do rosto, e a SENet aprende onde estão as características significativas. Na LANet e na DFA, os parâmetros dos experimentos são os de [6]. O desempenho da LANet ou da DFA isoladas não é tão bom quanto o dos outros métodos da Tabela 2. Uma razão possível é que o número de canais da rede é pequeno demais e, depois da compressão na LANet, a informação útil é drasticamente reduzida, diminuindo o desempenho. O desempenho do EFA nas bases entre poses e entre idades melhora significativamente em relação aos outros métodos, exceto na base CPLFW. Uma explicação possível é que dividimos os canais em grupos diferentes, com o parâmetro $g$, no EFA, de modo que a SENet dentro do EFA não consegue aproveitar bem a informação global dos canais, o que deixa o EFA um pouco pior na CPLFW do que a SENet sozinha. Assim, usar a SENet e a LANet ao mesmo tempo melhora o desempenho em relação a usar um módulo antes do outro. Como mostra a Tabela 2, em comparação com os outros métodos, o EFA equilibra acurácia e complexidade, melhorando o desempenho.

#### 3) Efeito dos parâmetros g e r no modelo

Para investigar o efeito dos parâmetros $g$ e $r$ do módulo EFA na fusão de SENet e LANet, faz-se o estudo a seguir, cujos resultados aparecem na Tabela 3.

> [Tabela 3: Comparação de desempenho entre diferentes combinações de valores de g e r em bases diferentes. Valores no PDF original.]

O hiperparâmetro $g$ assume os valores 2, 4, 8 e 16. O desempenho geral aumenta quando $g$ diminui. Isso pode ser explicado porque dividir os dados em grupos demais faz a rede dar mais atenção a informação inútil ou ruidosa. Para investigar a relação entre custo computacional e desempenho causada pelo hiperparâmetro de redução $r$, ele assume os valores 2, 4, 8 e 16. Porém, nos experimentos, a quantidade de cálculos e de parâmetros do modelo também depende do parâmetro $g$. O desempenho geral do modelo piora quando não se usa convolução em grupo, em comparação com o caso com convolução em grupo. Por fim, escolhem-se $g = 2$ e $r = 2$ para equilibrar desempenho e complexidade.

#### 4) Diferentes métodos de integração

Somar ou concatenar as características diretamente é o método escolhido pela maioria das abordagens de fusão de características. Porém, a soma ou a concatenação simples não conseguem fundir a informação entre camadas. Para superar esse problema, usa-se a ASFF para fundir a informação entre camadas.

A Tabela 4 mostra os resultados da comparação da ASFF com outros métodos de fusão. Em comparação com a soma e a concatenação, os ganhos da ASFF na base CPLFW são de 0,55% e 0,6%, respectivamente; na base CALFW, de 0,45% e 0,54%. Isso mostra as vantagens da ASFF em captar características entre camadas e em aprender pesos de forma adaptativa. No entanto, a ASFF não é tão boa quanto a concatenação em bases com grandes variações de pose, como VGG2(FP) e CFP(FP). Em geral, diante de grandes variações de pose, precisamos de mais canais para extrair informação de características mais rica. Nos nossos experimentos, a concatenação produz o maior número de canais e, por isso, tem o melhor desempenho nesse caso.

> [Tabela 4: Comparação de desempenho entre diferentes métodos de fusão em bases diferentes. Valores no PDF original.]

### D. Comparação com diferentes redes de base

Várias CNNs populares são comparadas com a ELANet, incluindo redes leves de reconhecimento facial e redes grandes e complexas. Os resultados aparecem na Tabela 5. Os resultados dos modelos leves de reconhecimento facial nas diferentes bases vêm de [35].

> [Tabela 5: Comparação de desempenho entre diferentes modelos de CNN em bases diferentes. Valores no PDF original.]

Em comparação com esses modelos leves, a ELANet obtém uma melhora geral de desempenho com apenas um pequeno aumento da complexidade computacional. Em particular, nas bases entre poses CPLFW, VGG2_FP e CFP_FP, o desempenho da ELANet melhorou 1,83%, 2,17% e 0,26%, respectivamente, em relação aos melhores modelos leves de reconhecimento facial. Na base entre idades CALFW, a ELANet melhorou 0,92% em relação aos melhores modelos leves. Em comparação com a ResNet-50 [37] e a DenseNet [36], a ELANet tem menos parâmetros e menos esforço computacional e desempenho melhor. Assim, a ELANet demonstra melhor eficiência de parâmetros. A ResNet aumenta a expressividade do modelo por meio de conexões de atalho, e a DenseNet melhora o desempenho com conexões densas. A EfficientNet [38] otimiza a expressividade do modelo em três aspectos ao mesmo tempo: profundidade, largura e resolução da rede. Ao usar convolução separável em profundidade, a MobileNet reduz os parâmetros do modelo, e uma estrutura residual invertida é usada para melhorar a representação. Assim, a ELANet continua usando o gargalo da MobileNet-V2 para reduzir o número de parâmetros e integra o módulo EFA ao gargalo, permitindo aprender a informação de regiões locais. O módulo EFA tem melhor desempenho e menos parâmetros de fusão. Diferentes níveis de informação são usados e fundidos pela ASFF para melhorar o desempenho do modelo. O módulo EFA proposto permite à ELANet focar mais nas características mais discriminativas diante de mudanças de pose; por isso, a ELANet se sai melhor em bases com várias mudanças de pose.

Em resumo, a ELANet tem boa capacidade de representação, usa bem os parâmetros, funciona bem com distribuições de dados complexas e equilibra bem acurácia e complexidade. Mais importante, tem poucos cálculos e poucos parâmetros, o que a torna muito adequada para dispositivos embarcados com baixo poder computacional.

### E. Experimentos entre poses

Nos experimentos entre poses, as bases MS1MV3 e VGGFace2 são usadas como dados de treino. A comparação entre a ELANet e métodos de ponta aparece na Tabela 6.

> [Tabela 6: Avaliação de desempenho nas bases entre poses. Valores no PDF original.]

A PIM [41] propõe uma rede adversarial generativa de duas vias, que aprende informação local e global, e uma sub-rede de aprendizado discriminativo, que aprende representações discriminativas e genéricas, alcançando 93,10% na base CFP_FP. A DA-GAN [42] gera imagens de alta resolução com uma rede totalmente convolucional e usa o autocodificador como discriminador com duplo agente. A p-CNN [43] usa uma rede neural convolucional multitarefa que agrupa poses diferentes para aprender características de identidade específicas de cada pose, obtendo 94,39%. A NoiseFace [44] é treinada com muitos dados ruidosos e obtém 96,04%. A LS-CNN [6] aprende informação de características locais e em múltiplas escalas, melhorando o desempenho para 97,17% na CFP_FP. A HDPA [8] obtém 92,35% na base CPLFW com aprendizado guiado multivariado. A DLL [45] propõe uma perda de destilação de distribuição para melhorar o desempenho em amostras difíceis, alcançando desempenho de ponta nas bases CFP_FP e CPLFW. A ELANet é simples e eficiente em comparação com métodos de aumento de dados muito complexos (PIM, DA-GAN), e obtém desempenho muito bom nas bases entre poses. Em comparação com a rede grande e complexa LS-CNN, a ELANet obtém desempenho semelhante com poucos parâmetros e pouco esforço computacional. Em comparação com os métodos de ponta, a ELANet obtém desempenho próximo do melhor com um modelo leve; em comparação com os modelos leves de reconhecimento facial propostos nos últimos anos, a ELANet os supera nas bases entre poses.

### F. Experimentos entre idades

Nos experimentos entre idades, as bases MS1MV3 e VGGFace2 são usadas como dados de treino. A ELANet é comparada com outros métodos de ponta na base CALFW na Tabela 7.

> [Tabela 7: Avaliação de desempenho na base entre idades. Valores no PDF original.]

A VGGFace [46] e a CCL [47] são treinadas com funções de perda avançadas. A VGGFace é treinada com a *triplet loss*. A CCL distribui as características do rosto em um espaço de coordenadas e divide os vetores de classificação na hiperesfera. A AFJT-CNN [48] treina de forma alternada uma rede de fusão e combina um modelo de fatores. A ELANet proposta é muito melhor que esses métodos nas bases entre idades. Em comparação com a LS-CNN, o módulo EFA proposto na ELANet consegue focar em regiões mais discriminativas do rosto. A HDPA alcança desempenho de ponta com aprendizado guiado multivariado, mas a rede como um todo é tão complexa que é difícil implementá-la em dispositivos embarcados ou móveis. Em contraste, a ELANet usa menos parâmetros e um método simples e eficaz para alcançar desempenho ótimo.

### G. Experimentos nas bases IJB-B/C

Esta seção compara o desempenho da ELANet com vários outros métodos nas bases IJB-B/C. Os resultados dos modelos ResNet50 [37], MN-v [49], MN-vc [49] e DCN [50] vêm de [3]. Usamos a ArcFace [3] para fazer os mesmos experimentos.

> [Tabela 8: Avaliação de desempenho nas bases IJB-B e IJB-C. Valores no PDF original.]

Este experimento compara a taxa de aceitação verdadeira (TAR) com taxa de falsa aceitação (FAR) de 10⁻⁴ da ELANet com a dos modelos de ponta, como mostra a Tabela 8. Com exceção da VarGFaceNet, a ELANet tem desempenho um pouco melhor nas IJB-B/C que qualquer outro modelo leve de reconhecimento facial. A ELANet tem desempenho semelhante ao das redes complexas nas IJB-B/C, exceto a ResNet100. Isso mostra a necessidade de introduzir características locais e informação de várias camadas e escalas no reconhecimento facial. Mostra também que usar informação de camadas diferentes para extrair características em conjunto é útil para o reconhecimento facial. Na Figura 8, mostramos as curvas ROC (*receiver operating characteristic*) da ELANet nas bases IJB-B e IJB-C.

> [Figura 8: Curvas ROC nas bases IJB-B e IJB-C.]

## V. Conclusão

Propõe-se uma abordagem eficaz para enfrentar o desafio do impacto da pose e da idade no desempenho do reconhecimento facial. Uma nova estrutura de rede leve, baseada na MobileFaceNet, é proposta: ela aprende características ricas em múltiplas escalas e em vários níveis, além de características locais discriminativas; atribui pesos diferentes a diferentes canais e características espaciais; e une níveis diferentes de características para o reconhecimento facial. O modelo ELANet generaliza em várias bases e alcança alto desempenho com menos parâmetros e cálculos do que outras abordagens, sendo ideal para implantação em dispositivos móveis e embarcados. Os experimentos mostram que a ELANet melhora significativamente o desempenho em relação a outras redes leves de ponta. A ELANet alcança desempenho semelhante ao de um modelo complexo e até melhor em algumas bases de teste. No futuro, a ELANet será testada em implantações reais em dispositivos móveis ou embarcados, para otimizar ainda mais o desempenho do modelo.

## Referências

As referências estão no idioma original.

[1] F. Schroff, D. Kalenichenko, J. Philbin, "FaceNet: A unified embedding for face recognition and clustering," CVPR, 2015, pp. 815–823.
[2] S. Chen, Y. Liu, X. Gao, Z. Han, "MobileFaceNets: Efficient CNNs for accurate real-time face verification on mobile devices," Chinese Conference on Biometric Recognition, Springer, 2018, pp. 428–438.
[3] J. Deng, J. Guo, N. Xue, S. Zafeiriou, "ArcFace: Additive angular margin loss for deep face recognition," CVPR, 2019, pp. 4690–4699.
[4] C. Ding, D. Tao, "Trunk-branch ensemble convolutional neural networks for video-based face recognition," IEEE TPAMI, vol. 40, no. 4, pp. 1002–1014, 2017.
[5] Y. Sun, Deep Learning Face Representation by Joint Identification-Verification, Chinese Univ. Hong Kong, 2015.
[6] Q. Wang, G. Guo, "LS-CNN: Characterizing local patches at multiple scales for face recognition," IEEE Trans. Inf. Forensics Security, vol. 15, pp. 1640–1653, 2020.
[7] J. Hu, L. Shen, G. Sun, "Squeeze-and-excitation networks," CVPR, 2018, pp. 7132–7141.
[8] Q. Wang, T. Wu, H. Zheng, G. Guo, "Hierarchical pyramid diverse attention networks for face recognition," CVPR, 2020, pp. 8326–8335.
[9] S.-H. Gao et al., "Res2Net: A new multi-scale backbone architecture," IEEE TPAMI, vol. 43, no. 2, pp. 652–662, 2021.
[10] Y. Zhou, Y. Liu, G. Han, Z. Zhang, "Face recognition based on global and local feature fusion," IEEE SSCI, 2019, pp. 2771–2775.
[11] M. Sandler et al., "MobileNetV2: Inverted residuals and linear bottlenecks," CVPR, 2018, pp. 4510–4520.
[12] K. Zhang, Z. Zhang, Z. Li, Y. Qiao, "Joint face detection and alignment using multitask cascaded convolutional networks," IEEE Signal Process. Lett., vol. 23, no. 10, pp. 1499–1503, 2016.
[13] N. K. Mishra, M. Dutta, S. K. Singh, "Multiscale parallel deep CNN (mpdCNN) architecture for the real low-resolution face recognition for surveillance," Image Vis. Comput., vol. 115, 104290, 2021.
[14] M. He et al., "Deformable face net for pose invariant face recognition," Pattern Recognit., vol. 100, 107113, 2020.
[15] J. Fu et al., "Dual attention network for scene segmentation," CVPR, 2019, pp. 3146–3154.
[16] Z. Tan et al., "Attention-based pedestrian attribute analysis," IEEE TIP, vol. 28, no. 12, pp. 6126–6140, 2019.
[17] J. Wang, S. Li, F. Luo, "Cross-age face recognition using deep learning model based on dual attention mechanism," Int. Conf. Commun., Signal Process., Syst., Springer, 2020, pp. 1911–1919.
[18] J. Liao, A. Kot, T. Guha, V. Sanchez, "Attention selective network for face synthesis and pose-invariant face recognition," ICIP, 2020, pp. 748–752.
[19] J. Yang et al., "Neural aggregation network for video face recognition," CVPR, 2017, pp. 4362–4371.
[20] W. Liu, L. Zhou, J. Chen, "Face recognition based on lightweight convolutional neural networks," Information, vol. 12, no. 5, p. 191, 2021.
[21] X. Li et al., "A discriminative self-attention cycle GAN for face super-resolution and recognition," IET Image Process., vol. 15, no. 11, pp. 2614–2628, 2021.
[22] A. G. Howard et al., "MobileNets: Efficient convolutional neural networks for mobile vision applications," arXiv:1704.04861, 2017.
[23] N. Ma, X. Zhang, H.-T. Zheng, J. Sun, "ShuffleNet V2: Practical guidelines for efficient CNN architecture design," ECCV, 2018, pp. 116–131.
[24] S. Liu, D. Huang, Y. Wang, "Learning spatial fusion for single-shot object detection," arXiv:1911.09516, 2019.
[25] J. Deng et al., "Lightweight face recognition challenge," ICCVW, 2019, pp. 1–9.
[26] Q. Cao, L. Shen, W. Xie, O. M. Parkhi, A. Zisserman, "VGGFace2: A dataset for recognising faces across pose and age," IEEE FG, 2018, pp. 67–74.
[27] Y. Guo et al., "MS-Celeb-1M: A dataset and benchmark for large-scale face recognition," ECCV, Springer, 2016, pp. 87–102.
[28] G. B. Huang, M. Mattar, T. Berg, E. Learned-Miller, "Labeled faces in the wild: A database for studying face recognition in unconstrained environments," Workshop Faces 'Real-Life' Images, 2008, pp. 1–15.
[29] T. Zheng, W. Deng, J. Hu, "Cross-age LFW: A database for studying cross-age face recognition in unconstrained environments," arXiv:1708.08197, 2017.
[30] T. Zheng, W. Deng, "Cross-pose LFW: A database for studying cross-pose face recognition in unconstrained environments," Beijing Univ. Posts Telecommun., Tech. Rep. 18-01, 2018.
[31] S. Sengupta et al., "Frontal to profile face verification in the wild," WACV, 2016, pp. 1–9.
[32] C. Whitelam et al., "IARPA Janus benchmark-B face dataset," CVPRW, 2017, pp. 90–98.
[33] A. Paszke et al., "PyTorch: An imperative style, high-performance deep learning library," NeurIPS, vol. 32, 2019, pp. 8026–8037.
[34] H. Wang et al., "CosFace: Large margin cosine loss for deep face recognition," CVPR, 2018, pp. 5265–5274.
[35] Y. Martinez-Diaz et al., "Benchmarking lightweight face architectures on specific face recognition scenarios," Artif. Intell. Rev., vol. 54, pp. 6201–6244, 2021.
[36] G. Huang, Z. Liu, L. Van Der Maaten, K. Q. Weinberger, "Densely connected convolutional networks," CVPR, 2017, pp. 4700–4708.
[37] K. He, X. Zhang, S. Ren, J. Sun, "Deep residual learning for image recognition," CVPR, 2016, pp. 770–778.
[38] M. Tan, Q. Le, "EfficientNet: Rethinking model scaling for convolutional neural networks," ICML, 2019, pp. 6105–6114.
[39] Y. Martinez-Diaz et al., "ShuffleFaceNet: A lightweight face architecture for efficient and highly-accurate face recognition," ICCVW, 2019, pp. 1–8.
[40] M. Yan et al., "VarGFaceNet: An efficient variable group convolutional neural network for lightweight face recognition," ICCVW, 2019, pp. 1–8.
[41] J. Zhao et al., "Towards pose invariant face recognition in the wild," CVPR, 2018, pp. 2207–2216.
[42] J. Zhao et al., "3D-aided dual-agent GANs for unconstrained face recognition," IEEE TPAMI, vol. 41, no. 10, pp. 2380–2394, 2019.
[43] X. Yin, X. Liu, "Multi-task convolutional neural network for pose-invariant face recognition," IEEE TIP, vol. 27, no. 2, pp. 964–975, 2018.
[44] W. Hu, Y. Huang, F. Zhang, R. Li, "Noise-tolerant paradigm for training face recognition CNNs," CVPR, 2019, pp. 11887–11896.
[45] Y. Huang et al., "Improving face recognition from hard samples via distribution distillation loss," ECCV, Springer, 2020, pp. 138–154.
[46] O. M. Parkhi, A. Vedaldi, A. Zisserman, "Deep face recognition," BMVC, 2015, pp. 41.1–41.12.
[47] X. Qi, L. Zhang, "Face recognition via centralized coordinate learning," arXiv:1801.05678, 2018.
[48] H. Li, H. Hu, C. Yip, "Age-related factor guided joint task modeling convolutional neural network for cross-age face recognition," IEEE Trans. Inf. Forensics Security, vol. 13, no. 9, pp. 2383–2392, 2018.
[49] W. Xie, A. Zisserman, "Multicolumn networks for face recognition," arXiv:1807.09192, 2018.
[50] W. Xie, L. Shen, A. Zisserman, "Comparator networks," ECCV, 2018, pp. 782–797.

## Sobre os autores

- **Peng Zhang** é doutor em Projeto e Fabricação Mecânica e Automação pela Lanzhou University of Technology e professor associado da Escola de Instrumentação e Eletrônica da North University of China. Pesquisa mesas de simulação multifuncionais, plataformas de estabilização, dispositivos inerciais, navegação inercial, controle colaborativo de múltiplos VANTs e sistemas inteligentes de sensoriamento.
- **Feng Zhao** nasceu em 1996, graduou-se em Engenharia de Informação Eletrônica pela North University of China em 2020, onde faz mestrado. Pesquisa detecção e reconhecimento de objetos.
- **Peng Liu** é doutor em Ciência e Engenharia de Controle pela Southeast University e publicou 11 artigos.
- **Mengwei Li** foi pós-doutorando no Instituto de Microeletrônica da Tsinghua University de 2011 a 2016 e publicou mais de 100 artigos.

---

## Notas para o TCC

*Seção acrescentada nesta tradução; não faz parte do artigo original.*

- **Por que importa:** é um exemplo de rede leve (baseada na MobileFaceNet) treinada com a perda ArcFace, pensada para dispositivos embarcados. Ajuda a explicar, na monografia, que "ArcFace" é a função de perda e não uma rede específica (item E1 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).
- **Por que crianças e ônibus:** o foco do artigo é robustez a pose e idade, dois problemas reais na porta do ônibus (alunos entrando de lado, rostos de crianças mudando ao longo do ano letivo).
- **O que falta:** o artigo não mede tempo em hardware embarcado; a afirmação "adequada para embarcados" vem só da contagem de parâmetros e operações (Tabela 5 do PDF). O mesmo grupo publicou depois o DGFaceNet (Zhao *et al.*, 2023), que também está na pasta.
- **Bases citadas:** CALFW (entre idades) e CPLFW (entre poses) são variantes da LFW e podem servir para a ampliação da base prevista no benchmark.
