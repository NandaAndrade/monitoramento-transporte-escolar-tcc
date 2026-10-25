# Um modelo leve de aprendizado profundo para reconhecimento facial em tempo real

> **Tradução integral para o português**, feita para estudo do TCC.
>
> **Original:** DENG, Z.-Y.; CHIANG, H.-H.; KANG, L.-W.; LI, H.-C. A lightweight deep learning model for real-time face recognition. *IET Image Processing*, v. 17, p. 3869–3883, 2023. DOI: [10.1049/ipr2.12903](https://doi.org/10.1049/ipr2.12903).
>
> **Licença:** o original é publicado em acesso aberto sob a licença [Creative Commons Atribuição (CC BY)](https://creativecommons.org/licenses/by/4.0/deed.pt-br), © 2023 os autores; publicado por John Wiley & Sons Ltd em nome da The Institution of Engineering and Technology. Esta tradução é uma obra derivada: o texto foi traduzido do inglês, as figuras foram substituídas por suas legendas e foram acrescentadas notas da tradução, marcadas como **[N. T.]**, e a seção final "Notas para o TCC". Os autores originais não revisaram nem endossam esta tradução.
>
> **PDF local:** `Downloads/Referencias/deng_2023_modelo_leve_reconhecimento_facial_tempo_real.pdf`

---

**Zong-Yue Deng¹, Hsin-Han Chiang², Li-Wei Kang¹ e Hsiao-Chi Li³**
¹ Departamento de Engenharia Elétrica, National Taiwan Normal University, Taipei, Taiwan.
² Departamento de Engenharia de Veículos, National Taipei University of Technology, Taipei, Taiwan.
³ Departamento de Engenharia Elétrica, National Taipei University of Technology, Taipei, Taiwan.
Recebido em 24 fev. 2023; revisado em 22 jun. 2023; aceito em 30 jul. 2023.
Financiamento: National Science and Technology Council, projetos 109-2221-E-027-124-MY3 e 111-2221-E-027-147-MY2.

## Resumo

Modelos leves de aprendizado profundo para reconhecimento facial estão se tornando cada vez mais importantes para a implantação em dispositivos com poucos recursos, como sistemas embarcados ou dispositivos móveis. Este artigo apresenta um modelo de aprendizado profundo (DL) altamente eficiente e compacto, que alcança desempenho de ponta em vários *benchmarks* de reconhecimento facial. O modelo desenvolvido usa aprendizado com um ou poucos exemplos (*one-shot* ou *few-shot*) para obter *embeddings* de características eficazes e se inspira no FaceNet, com refinamentos significativos, para chegar a um tamanho em memória de apenas 3,5 MB, cerca de 30 vezes menor que o FaceNet, mantendo alta acurácia e desempenho em tempo real. O estudo demonstra a eficácia do modelo por meio de experimentos extensos, que incluem testes em bases públicas e a capacidade do modelo de reconhecer rostos parcialmente cobertos em ambientes não controlados, usando imagens de entrada em tons de cinza. Em comparação com os modelos leves de ponta, o modelo proposto exige menos FLOPs (0,06 G), tem menos parâmetros (1,2 M) e ocupa menos espaço (3,5 MB), alcançando nível competitivo de acurácia de reconhecimento e desempenho em tempo real. Os resultados mostram que o modelo é bem adequado para implantação em domínios embarcados, incluindo controle de acesso ao vivo em entradas, autorização de motoristas e sistemas de presença em sala de aula. Todo o código do FN8 está disponível no GitHub.

## 1 Introdução

As técnicas de aprendizado profundo (DL) se tornaram um método promissor para alcançar reconhecimento facial de ponta, graças ao desempenho impressionante em *benchmarks* públicos. Para extrair características valiosas de bases faciais, arquiteturas em evolução com funções de perda adequadas são cruciais para um reconhecimento facial robusto. No entanto, a acurácia dos algoritmos de DL depende muito de bases de grande escala com dados de treino bem anotados, o que pode tornar os modelos profundos de reconhecimento facial grandes, complexos e difíceis de implantar em plataformas embarcadas com recursos computacionais limitados. Para enfrentar esse desafio, pesquisadores têm se concentrado em desenvolver métodos de reconhecimento facial eficientes e leves, incluindo o FaceNet, que recebeu atenção pela alta acurácia e pela robustez a vários fatores [1].

Até agora, muitos trabalhos de pesquisa avançaram as aplicações específicas do FaceNet e de outros modelos de ponta [2–5]; porém, eles costumam depender de GPUs sofisticadas e de grandes bases, o que pode limitar seu desempenho. Além disso, muitos algoritmos baseados em DL se concentram em melhorar a acurácia de reconhecimento sem considerar a redução do tamanho do modelo e da escala do algoritmo. Para equilibrar desempenho de ponta e tamanho do modelo, é essencial desenvolver um modelo de DL leve que alcance altos níveis de acurácia e compacidade.

No presente estudo, tratamos essas questões desenvolvendo um modelo de DL excepcionalmente leve e eficiente, como solução prática para um reconhecimento facial preciso e robusto, sem comprometer o desempenho. As contribuições principais deste trabalho são:

- O estudo propõe um modelo de DL extremamente leve para reconhecimento facial, com apenas 3,5 MB, 2,3 vezes mais leve que o MobileFaceNet. O desempenho do modelo é avaliado em termos de acurácia, eficiência e robustez para rostos parcialmente cobertos, mesmo em ambientes não controlados. **[N. T.: pela Tabela 4, o MobileFaceNet tem 4 MB, o que não corresponde a 2,3 vezes os 3,5 MB do FN8.]**
- Os conceitos apresentados são essenciais para alcançar desempenho de ponta com recursos computacionais muito menores. Eles incluem *embeddings* faciais obtidos pela modificação da estrutura da Inception ResNet, correspondências impostas por *pooling* de média global (GAP) e o projeto da saída da rede.
- O estudo analisa e compara a capacidade de implantação do modelo leve proposto com os modelos de ponta em termos de tamanho do modelo, número de parâmetros, bilhões de operações de ponto flutuante (GFLOPs) e recursos de hardware.
- Em comparação com os modelos de ponta existentes, o modelo desenvolvido é menor e tem menor custo computacional, enquanto o desempenho de reconhecimento alcança acurácia competitiva e capacidade de tempo real. O modelo proposto também pode ser treinado para aplicações reais da comunidade de reconhecimento facial e implantado de forma eficaz em dispositivos com poucos recursos.

O artigo está estruturado assim. Primeiro, a Seção 2 apresenta uma visão geral dos trabalhos relacionados. Depois, a Seção 3 apresenta a implementação específica do modelo leve de reconhecimento proposto. A Seção 4 traz uma avaliação experimental extensa e a comparação com os modelos faciais leves selecionados. Por fim, a Seção 5 apresenta as conclusões.

## 2 Trabalhos relacionados

Recentemente, muitos pesquisadores demonstraram a confiabilidade de seus modelos de reconhecimento facial na identificação de pessoas. Esses modelos podem ser aplicados a vários cenários reais, como controle e monitoramento de segurança, controle de acesso em portões, verificação do uso correto de máscara e identificação de rostos com máscara [6–10]. Executar esses programas em dispositivos de computação de alto desempenho (HPC) não é problema, mas eles frequentemente enfrentam recursos computacionais limitados. Esta seção resume as soluções existentes de reconhecimento facial e os avanços relacionados em arcabouços de estrutura leve.

### 2.1 Reconhecimento facial

O reconhecimento facial busca identificar a identidade de uma pessoa. Os desafios incluem oclusão, imagens de baixa qualidade, mudanças de postura, variações do ângulo da cabeça e condições de iluminação. Muitos estudos se concentraram e discutiram intensamente, nas últimas décadas, três subdomínios para construir essas tarefas de reconhecimento: detecção de rostos, extração de características faciais e casamento de rostos [7, 11–14]. Em vez de realizar o reconhecimento facial por esses arcabouços tradicionais de vários estágios separados, as técnicas de redes neurais convolucionais (CNN) fizeram a área avançar ao realizar a extração e a classificação em uma única rede, sem necessidade de características faciais predefinidas. O DeepFace [15], com base AlexNet, o DeepID [16] e o VGG-Face [17], com base VGGNet, foram propostos para extrair características faciais usando redes neurais convolucionais profundas, com camadas totalmente conectadas atuando como classificador. Ainda assim, outros acreditam que uma rede mais profunda pode fornecer características mais detalhadas, mas pode não ser boa para discernir diferenças sutis entre classes e grandes variações dentro da mesma classe. Por isso, aplicar CNNs profundas de ponta, como AlexNet, GoogleNet, ResNet etc., junto com um classificador convencional, a máquina de vetores de suporte (SVM), é uma solução para lidar com os diferentes fatores de oclusão, pose ou iluminação e alcançar maior acurácia [18].

A estrutura mais recente introduz uma estratégia de aprendizado com poucos exemplos, que gera *embeddings* de características por meio de camadas convolucionais e realiza a identificação do rosto pela similaridade com os rostos armazenados. O FaceNet, proposto pelo grupo de pesquisa do Google, é um dos modelos mais representativos da literatura. Com sua rede profunda, o FaceNet extrai as características faciais como um *embedding* e realiza um reconhecimento preciso, com grande sucesso e acurácia de 99% na base Labeled Faces in the Wild (LFW), com o processo de geração do *embedding* aprendido e supervisionado pela *triplet loss*. Mesmo assim, o FaceNet tem o defeito do grande tamanho do modelo. Por isso, muitas variantes de redes de reconhecimento facial foram modificadas e herdadas do FaceNet, como OpenFace [19], MobiFace [20] e ShuffleFaceNet [21], para enfrentar esse peso computacional. Além disso, SphereFace [22], CosFace [23] e ArcFace [24] se concentraram em melhorar o reconhecimento em várias poses, iluminações e oclusões, encontrando margens adequadas com distância angular.

### 2.2 Aplicações leves de aprendizado profundo

Apesar da acurácia excepcional dos modelos de reconhecimento que incorporam DL, a ineficiência computacional os torna inadequados para aplicações reais. Isso ocorre porque os dispositivos embarcados não conseguem sustentar as aplicações de DL em tempo real mantendo baixa latência, baixo consumo de energia e alta precisão sob essas restrições de recursos. Assim, é necessária uma estratégia prática, como compromisso entre a generalização e o desempenho do modelo. Para tratar essa questão, vários pesquisadores propuseram modelos de reconhecimento leves e eficientes. Duong *et al.* e Martínez-Díaz *et al.* propuseram, respectivamente, o MobiFace e o ShuffleFaceNet, para manter a acurácia de identificação com estruturas mais leves que o FaceNet. Outra arquitetura leve é o VarGFaceNet [25], que reduziu o VarGNet alternando o uso de blocos com um bloco de compressão e excitação (SE). O MobileFaceNet [26] combinou a MobileNet com a perda ArcFace para obter reconhecimento facial leve. Kocacinar *et al.* [27] usaram a MobileNet como modelo pré-treinado para melhorar o desempenho na identificação de rostos com máscara. O ELANet [28], inspirado no MobileFaceNet, enfrenta o desafio das variações faciais incorporando mecanismos de atenção espacial e um módulo piramidal de múltiplas escalas para captar características em escalas diferentes. O PocketNet, um modelo estudante, aprende com a ResNet-100 como modelo professor, usando o algoritmo de busca diferencial de arquiteturas (DARTS) [29]. O ConvFaceNeXt usa um bloco ConvNeXt aprimorado (ECN) com convolução em profundidade na primeira camada [30] para reduzir FLOPs e o número de parâmetros. Martínez-Díaz *et al.* [31] aplicaram e avaliaram três modelos leves de reconhecimento facial no desafio de reconhecimento de rostos com máscara. Zhao *et al.* [32] apresentaram uma CNN leve que incorpora uma camada convolucional densamente conectada com técnicas de compressão de modelo para reconhecimento de emoção e expressão. Agbo-Ajala e Viriri [33] ofereceram um modelo leve para estimar a idade real e aparente e o implantaram em dispositivos móveis. Sun *et al.* [10] apresentaram uma solução leve com CNN para detectar a pose da cabeça na taxa de vídeo. Wang *et al.* [14] simplificaram a CNN alternando camadas convolucionais com padrões binários locais (LBP) e análise de componentes principais (PCA), para eliminar o longo tempo de treinamento das CNNs profundas no reconhecimento de vários rostos.

## 3 Método proposto

O arcabouço do método proposto tem dois componentes principais: uma série de etapas de pré-processamento de imagem e um modelo de reconhecimento. Esta pesquisa busca eliminar a redundância do modelo e otimizar seu desempenho, mantendo uma taxa de reconhecimento precisa. Para isso, serão apresentados a arquitetura do modelo de reconhecimento proposto, baseado em CNN, os algoritmos de otimização, as etapas de pré-processamento de imagem e a escolha das funções de perda. Esta seção também detalha o processo de treinamento do modelo. Espera-se que essa abordagem permita o processamento embarcado de dados em tempo real, como ilustra a Figura 1.

> [Figura 1: Processo geral do reconhecimento facial profundo proposto, na fase de treinamento e na fase de teste em tempo real.]

### 3.1 Pré-processamento

O objetivo deste estudo é reduzir o tamanho da rede de reconhecimento facial sem comprometer sua acurácia. Para isso, o artigo propõe um modelo que recebe imagens em tons de cinza como entrada. Para extrair as características essenciais do rosto, aplicam-se várias etapas de processamento de imagem, incluindo registro/detecção do rosto com características do tipo Haar, equalização de histograma para realçar o contraste, realce do contorno/bordas do rosto e aumento de dados de imagem. O aumento de dados envolve processos como branqueamento (*whitening*), rotação aleatória, mudança de escala aleatória e espelhamento aleatório.

### 3.2 Modelo de reconhecimento

Este estudo parte do arcabouço do FaceNet e usa uma série de estratégias de simplificação para desenvolver um modelo de reconhecimento reduzido, chamado FN8.

#### 3.2.1 Estrutura do modelo

A Figura 2 mostra o modelo FN8 proposto, e sua estrutura detalhada aparece na Tabela 1. O modelo consiste principalmente em camadas convolucionais, convoluções separáveis e Inception ResNets refinadas, para extrair características faciais e gerar *embeddings* faciais para a classificação.

> [Figura 2: O modelo leve proposto para reconhecimento facial.]

**Tabela 1.** Arquitetura do modelo FN8 proposto para gerar *embeddings* faciais.

| Camada/passo | Núcleo | Tamanho da saída | Parâmetros |
|---|---|---|---|
| Imagem | – | 160 × 160 × 1 | – |
| Conv / 2 | 3 × 3 | 80 × 80 × 32 | 320 |
| Conv / 2 | 5 × 5 | 40 × 40 × 64 | 51,26 mil |
| Conv_Sep / 2 | 3 × 3 | 20 × 20 × 128 | 8,896 mil |
| Inception ResNet A | – | 20 × 20 × 128 | 754,43 mil |
| Inception ResNet B | – | 20 × 20 × 128 | 344,576 mil |
| Conv_Sep / 2 | 3 × 3 | 9 × 9 × 196 | 25,92 mil |
| Conv_Sep / 2 | 3 × 3 | 6 × 6 × 256 | 51,136 mil |
| GAP | 6 × 6 | 1 × 1 × 125 **[N. T.: assim no original; pelo restante do texto, o *embedding* tem 256 dimensões]** | 0 |
| Total | – | – | 1,24 M |

Para reduzir o tamanho dos mapas de características, usa-se passo 2 como alternativa ao *pooling*. Convoluções separáveis são usadas na 3ª, na 6ª e na 7ª camadas para minimizar o número de parâmetros da máscara de convolução. Nas camadas convolucionais da Inception ResNet-A refinada (Figura 3), filtros de tamanhos heterogêneos (3 × 5, 5 × 3 e 1 × 1) são projetados para captar várias combinações de características faciais. A informação espacial da entrada da Inception passa por *max-pooling* para reunir as características faciais principais. A entrada do processo Inception é então ligada por conexão de atalho às características Inception resultantes. Para evitar correções exageradas, as características Inception resultantes são multiplicadas por um fator de 0,1 antes da conexão de atalho.

Além disso, as características espaciais captadas pela Inception ResNet-A modificada passam à segunda estrutura, modificada a partir da Inception ResNet-B. O *max-pooling* é usado nesses dois módulos Inception para evitar sobreajuste. Ao incorporar a Inception ResNet-B, o FN8 consegue extrair autocaracterísticas detalhadas que poderiam ter sido perdidas. Além dessas modificações, o FN8 inclui apenas uma camada GAP, que substitui várias camadas totalmente conectadas convencionais, para extrair as características tridimensionais da imagem como um vetor de *embedding*.

> [Figura 3: Estruturas Inception refinadas. (a) Inception ResNet-A. (b) Inception ResNet-B.]

#### 3.2.2 Função objetivo

Nos últimos anos, a CNN se tornou a ferramenta mais popular para construir redes de discriminação, por extrair características sem intervenção manual, por meio do processo de convolução. Embora uma CNN convencional consiga distinguir facilmente objetos de classes diferentes com funções de perda simples, como a perda *softmax*, o reconhecimento facial é uma tarefa mais desafiadora. Mesmo que a *softmax* consiga diferenciar vários rostos, as diferenças entre as classes costumam ser insuficientes. Essa insuficiência pode fazer o reconhecimento falhar em tarefas difíceis. Além disso, a configuração de perda convencional das CNNs, composta pela *softmax* e pela entropia cruzada, traz vários problemas não resolvidos. Primeiro, exige um esforço computacional excessivo para treinar o modelo. Segundo, tem capacidade limitada de extrair características na camada totalmente conectada, especialmente quando é preciso distinguir muitas classes de rostos. Por último, o modelo não é reutilizável quando novas classes de rostos são acrescentadas ao sistema de reconhecimento, o que é um requisito crucial em tarefas de reconhecimento facial, sobretudo em aplicações reais. Também é essencial ter resposta imediata sem necessidade de retreinar o modelo, especialmente em sistemas de controle de acesso que cadastram novos usuários com frequência. Retreinar a rede de reconhecimento a cada cadastro de poucos usuários novos se torna impraticável.

A Figura 4a mostra as características de cada classe de rosto em um modelo treinado com perda *softmax*. Por causa das grandes variações dentro de uma mesma classe, o modelo resultante pode ter uma taxa de erro de classificação maior, sobretudo quando novas classes de rostos são introduzidas. Nessas circunstâncias, o modelo precisa ser atualizado. Por isso, o modelo proposto substitui a configuração conservadora da função de perda pela perda de centro (*center loss*) [34], supervisionada em conjunto com a *softmax*, para reduzir a variedade de características dentro de cada classe de rosto. Ao mesmo tempo, os centros das classes são atualizados com base no critério de otimização de Fisher. Sob a supervisão conjunta da perda *softmax* e da perda de centro, as amostras da mesma classe ficam mais próximas de seus centros, enquanto as diferentes classes de rostos se mantêm afastadas umas das outras. Consequentemente, isso não só reduz as variações das características dentro de cada classe, como também mantém as diferenças entre as classes. A Figura 4b mostra um exemplo com características em um espaço bidimensional e ilustra a combinação da perda de centro com a *softmax* para treinar o *embedding* das características faciais.

> [Figura 4: Comparação entre os vetores de *embedding* aprendidos pelo modelo sem e com a perda de centro combinada à *softmax*: (a) sem perda de centro; (b) com perda de centro. Pontos de cores diferentes representam características de classes diferentes.]

Para caracterizar a variação dentro da classe, partimos da função de perda de centro, formulada como:

$$L_c = \frac{1}{2}\sum_{i=1}^{m} \lVert x_i - c_{y_i} \rVert_2^2 \tag{1}$$

Nessa função, $m$ é o tamanho do lote, $x_i$ é o *embedding* extraído da $i$-ésima imagem e $c_{y_i}$ é o centro da classe $y_i$. Durante a atualização dos centros, o modelo fica mais eficiente usando apenas os lotes atuais e as classes correspondentes. A partir do gradiente de $L_c$ em relação a $x_i$, definido por $\partial L_c / \partial x_i = x_i - c_{y_i}$, a função de atualização $\Delta c_j$ da classe $c_j$ pode ser derivada como:

$$\Delta c_j = \frac{\sum_{i=1}^{m} \delta(y_i = j) \cdot (c_j - x_i)}{1 + \sum_{i=1}^{m} \delta(y_i = j)} \tag{2}$$

em que $\delta(\cdot)$ é a função de condição, satisfeita quando $y_i = j$. A função de perda *softmax* pode ser formulada como:

$$L_S = -\sum_{i=1}^{m}\sum_{j=1}^{n} \delta(y_i = j) \log \frac{e^{W^T x_i + b}}{\sum_{l=1}^{n} e^{W^T x_l + b}} \tag{3}$$

em que $n$ é o número de pessoas armazenadas na base, $W$ é o peso correspondente da última camada conectada do modelo e $b$ é o viés. No geral, a função objetivo que combina a perda de centro e a perda *softmax* no modelo FN8 proposto pode ser formulada como:

$$L = L_s + \lambda L_C \tag{4}$$

em que $\lambda$ denota o peso da perda de centro por classe.

#### 3.2.3 Normalização em lote e otimizador

O modelo FN8 proposto consegue reduzir muito o número de parâmetros e de cálculos. Mesmo assim, há dois problemas comuns que afetam a eficiência do treinamento. Primeiro, o modelo é sensível aos valores iniciais dos parâmetros e à escolha da taxa de aprendizado. Segundo, há o impacto dos cálculos em termos de precisão numérica no modelo de DL. À medida que a rede fica mais profunda, cada pequena flutuação de cálculo nas camadas continua aumentando. Por isso, aplica-se a normalização em minilote [35] para resolver esses problemas. Ela normaliza a entrada de cada camada, compensando o deslocamento interno de covariáveis (*internal covariate shift*), pela média e pela variância do minilote de tamanho $m$, denotado $x_i$, como em (5):

$$\hat{x}_i^{(k)} = \frac{x_i^{(k)} - \mu_B^{(k)}}{\sqrt{{\sigma_B^{(k)}}^2 + \epsilon}}, \quad \mu_B^{(k)} = \frac{1}{m}\sum_{i=1}^{m} x_i^{(k)}, \quad {\sigma_B^{(k)}}^2 = \frac{1}{m}\sum_{i=1}^{m}\left(x_i^{(k)} - \mu_B^{(k)}\right)^2 \tag{5}$$

em que $k$ representa o número do minilote, $\mu_B$ e $\sigma_B^2$ são a média e a variância da entrada da camada em cada minilote, respectivamente, e $\epsilon$ é uma constante. Para manter as características não lineares, as características normalizadas de um minilote são ativadas introduzindo os parâmetros $\gamma$ e $\beta$, que ajustam cada dimensão de característica e representam a saída da camada pela equação:

$$y_i^{(k)} = \gamma \hat{x}_i^{(k)} + \beta \tag{6}$$

Vale destacar algumas vantagens notáveis da normalização em lote no treinamento do modelo:

1. **Resolve o problema de gradientes que explodem ou desaparecem.** No treinamento, os gradientes ficam cada vez menores. Nesse ponto, o ajuste dos parâmetros se torna mais significativo para o modelo. Introduzir o minilote reescala os parâmetros e diminui a dependência dos gradientes.
2. **Convergência estável para o ótimo global.** O minilote pode levar a uma convergência mais estável, em que os gradientes calculados são a média de várias amostras, com menos ruído.
3. **Evita o sobreajuste.** Observações empíricas sugerem que lotes menores podem levar a uma dinâmica de treinamento mais rápida. Além disso, lotes menores tendem a melhorar a capacidade de generalização do modelo na base de teste em comparação com lotes maiores. Esse fenômeno pode ser atribuído à ideia de que lotes pequenos funcionam como representações ruidosas da base inteira. Assim, usar lotes pequenos introduz uma dinâmica de "cabo de guerra", que impede a rede neural de se ajustar demais ao conjunto de treino e, consequentemente, evita mau desempenho no conjunto de teste.

### 3.3 Treinamento do modelo

O modelo proposto se concentra em identificar rostos em tons de cinza para reconhecer rostos de forma eficiente entre várias classes. Primeiro, aplica-se uma transformação para tons de cinza, gerando uma imagem de um único canal como entrada do modelo. As imagens faciais pré-processadas pelas etapas citadas são então usadas para treinar o FN8, conforme o fluxograma da Figura 5. O FN8 tem uma camada de entrada em lote semelhante à do FaceNet, seguida da rede neural reduzida proposta, com estrutura significativamente mais leve. Assim, ao contrário do FaceNet, que exige muitos recursos computacionais no treinamento, o modelo proposto evita o sobreajuste sob a supervisão conjunta da perda de centro e da perda *softmax*. O modelo atualiza seus parâmetros por retropropagação com o otimizador ADAM, e o treinamento se repete até a perda média convergir e atingir o critério predefinido ou o número de épocas de treinamento. Assim, o modelo treinado gera um *embedding* facial de 256 entradas para cada imagem facial de entrada, exigindo ajuste mínimo de parâmetros no treinamento. Depois disso, adota-se a distância de Mahalanobis (MD) no modelo de reconhecimento para quantificar a similaridade e perceber a diferença entre as classes de rostos. Com o limiar ótimo determinado pela área sob a curva ROC (AUROC) para o classificador de reconhecimento, é possível determinar se a imagem facial de entrada existe na base. Confirmada a existência, o reconhecimento segue para identificar a pessoa: compara a distância entre o *embedding* da entrada e os dos rostos armazenados. Ordenando pela distância como medida de similaridade, o modelo considera de maior posição a classe de rosto com menor valor. Por fim, o classificador atribui o rosto à classe de maior posição.

> [Figura 5: Fluxograma de processamento do arcabouço de reconhecimento facial proposto.]

A rede proposta é projetada com base em uma estratégia de aprendizado com poucos exemplos [36]. Ao contrário do modelo de reconhecimento convencional, que gera a probabilidade de a pessoa pertencer a cada classe possível, ela incorpora toda a informação das características em um vetor, chamado *embedding* facial, e deixa a discriminação para uma etapa posterior. Aqui, o *embedding* facial tem papel essencial para reconhecer a pessoa com precisão, e o modelo, em particular, não precisa ser retreinado para nenhum rosto novo.

Como o FN8 usa várias funções de perda no treinamento, diferentemente do FaceNet, não é possível medir a similaridade dos *embeddings* como o FaceNet faz. O FaceNet, com a *triplet loss*, garante que a distância entre vetores de características da mesma classe seja menor que a distância entre vetores de classes diferentes. Por isso, o FaceNet não precisa se preocupar com a correlação entre as características. Diferentemente do FaceNet, o FN8 se dedica a separar ao máximo as amostras de classes diferentes, minimizando as variações dentro de cada classe. Com a escolha da MD em vez da distância euclidiana (ED), o FN8 consegue eliminar as correlações entre as características.

#### 3.3.1 Distância de Mahalanobis

A MD é uma medida de distância que quantifica de forma eficaz a similaridade de duas amostras. Usando a inversa da matriz de covariância amostral e a centralização dos dados, a MD mede a distância entre *embeddings* faciais correlacionados por:

$$md\left(f_{input}, f_c\right) = \left[\left(f_{input} - f_c\right)^T \Sigma^{-1} \left(f_{input} - f_c\right)\right]^{\frac{1}{2}} \tag{7}$$

em que $f_{input}$ é o *embedding* da imagem facial de entrada, $f_c$ é o centroide de todos os *embeddings* gerados a partir das amostras de treino e $\Sigma$ é a matriz de covariância amostral dos rostos de treino. Por ser uma matriz simétrica positiva semidefinida, a matriz de covariância amostral pode ser decomposta por autovalores como:

$$\Sigma = U \Lambda U^T \tag{8}$$

em que os vetores coluna $u_i$ de $U$ são os autovetores unitários e $\Lambda$ é a matriz diagonal dos autovalores. Assim, $\Sigma^{-1}$ pode ser derivada como:

$$\Sigma^{-1} = (U^T)^{-1}\Lambda^{-1}U^{-1} = U\Lambda^{-1}U^T = \left(U\Lambda^{-\frac{1}{2}}\right)\left(U\Lambda^{-\frac{1}{2}}\right)^T = \sum_{i=1}^{D} \lambda_i^{-1} u_i u_i^T \tag{9}$$

usando $U^{-1} = U^T$. Na Equação (9), $D$ representa a dimensão dos *embeddings* faciais gerados. Agora, a similaridade de dois *embeddings*, $f_1$ e $f_2$, pode ser medida por:

$$md^2(f_1, f_2) = (f_1 - f_2)^T\left(\sum_{i=1}^{D}\lambda_i^{-1}u_iu_i^T\right)(f_1 - f_2) = \sum_{i=1}^{D}\lambda_i^{-1}\left(u_i^T f_1 - u_i^T f_2\right)^2 \tag{10}$$

Como mostra a Equação (10), as correlações entre as características são reduzidas pela decomposição da matriz de covariância amostral. Assim, a MD entre dois *embeddings* faciais pode ser calculada de forma eficiente usando os autovetores unitários.

## 4 Resultados experimentais e avaliação

Este estudo realiza os experimentos em dois ambientes computacionais diferentes, um computador pessoal comum e um computador industrial, para implementar os modelos de reconhecimento facial propostos. Os resultados experimentais servem para verificar o desempenho. Os experimentos se dividem em duas partes. A primeira trata da configuração dos parâmetros do modelo na fase de treinamento, e a segunda, da avaliação do modelo na fase de teste. Para uma comparação justa, o FN8 foi treinado em um dispositivo com GPU e testado em dispositivos sem suporte a GPU.

### 4.1 Base de dados

Reconhecer rostos humanos com precisão em aplicações reais pode ser desafiador por causa de vários fatores ambientais, incluindo condições de iluminação, variações de temperatura e mudanças físicas relacionadas à idade. Para avaliar a eficácia do modelo proposto diante desses desafios, é crucial usar uma base cuidadosamente selecionada. A Labeled Faces in the Wild (LFW) [37] é uma base muito usada em tarefas de reconhecimento facial. Ela reúne um conjunto diverso de 13.233 imagens faciais, com variações de pose, expressão e iluminação, de 5.749 pessoas.

Além disso, a base AgeDB [38] permite a verificação facial invariante à idade e inclui 16.488 imagens faciais de 568 pessoas. Ela oferece anotações de idade sem ruído e tem 3.000 pares positivos e 3.000 pares negativos. Inclui quatro protocolos, com diferenças de idade de 5, 10, 20 e 30 anos, permitindo uma avaliação abrangente de técnicas de verificação facial relacionadas à idade. Na nossa avaliação, escolhemos o protocolo AgeDB-30, por ter a maior diferença de idade, o que é um cenário mais desafiador que os outros três protocolos.

Para demonstrar a capacidade discriminativa do modelo FN8, um subconjunto do conjunto de teste da LFW foi usado em um teste de similaridade. Os escores de similaridade vão de −1 a 1, e um valor próximo de 1 indica que as duas amostras provavelmente pertencem à mesma pessoa. Escores próximos de −1 podem ocorrer quando as duas amostras são da mesma pessoa, mas em posturas opostas. Como mostra a Figura 6, a maioria das amostras tem pouca relação entre si, com valores próximos de zero. A maior similaridade entre duas pessoas diferentes (fora da diagonal) é cerca de 0,26 (Abdel × Abbas). Isso ocorre porque as duas pessoas compartilham uma característica semelhante nas fotos: o uso de óculos escuros. O modelo de reconhecimento precisa se apoiar nas outras características extraídas, que formam um *embedding* facial distinto, para discriminar melhor amostras disfarçadas. Além disso, a Figura 6a mostra que o FN8 tem boa capacidade de separar rostos diferentes, já que a maioria dos escores de similaridade é próxima de zero.

> [Figura 6: (a) Teste de similaridade na base LFW com os *embeddings* faciais gerados pelo FN8; (b) as duas pessoas cujas fotos têm a maior correlação em (a).]

Para gerar um *embedding* facial para cada imagem, o modelo FN8 produziu um *embedding* de 256 dimensões. A escolha de 256 dimensões foi feita com base em análise empírica, discutida na Subseção 4.3.1. Pela Tabela 2, o FN8 com *embeddings* de 256 dimensões alcança maior acurácia que as saídas de 128 ou de 512 dimensões.

**Tabela 2.** Comparação da acurácia do modelo com diferentes dimensões de *embedding* facial.

| Dimensão | Acurácia | Medida F1 |
|---|---|---|
| 128 | 92,82% | 0,9405 |
| 256 | 98,40% | 0,9465 |
| 512 | 92,37% | 0,938 |

### 4.2 Resultados e avaliação

Nesta seção, apresentamos os resultados experimentais e a avaliação de desempenho do modelo FN8. Inicialmente, o FN8 foi treinado com a base CASIA-WebFace [39], e seu desempenho foi avaliado nas bases LFW e AgeDB. Em seguida, o desempenho do FN8 foi avaliado em um cenário de tempo real com a nossa base própria. Para demonstrar melhor a eficiência computacional superior do FN8, dois modelos leves de ponta foram usados como referência no teste com os dados próprios.

#### 4.2.1 Comparação de desempenho em bases públicas

O FN8 foi treinado na base CASIA-WebFace, com lotes de 128 na normalização em lote. O modelo alcançou uma acurácia impressionante de 99% na verificação da LFW, mostrando sua eficácia apesar da estrutura leve. As Figuras 7 e 8 mostram a acurácia e a evolução da perda do modelo, respectivamente, ao longo do treinamento com a perda de centro combinada à perda *softmax*. O uso do otimizador ADAM contribuiu para melhorar tanto a acurácia quanto a perda. Nota-se uma queda significativa da perda nas Figuras 8 e 9 quando a taxa de aprendizado foi ajustada para 10⁻³ na iteração 100.000.

> [Figura 7: Acurácia do modelo no treinamento.]
> [Figura 8: Evolução da perda de treinamento.]
> [Figura 9: Evolução da taxa de aprendizado.]

Na comparação de desempenho na base LFW, o FN8 superou o FaceNet em precisão e eficiência do modelo, tanto em dispositivos com bastante recurso computacional quanto em dispositivos com relativamente pouco recurso. Como mostra a Tabela 3, o FN8 manteve alta acurácia e reduziu significativamente o tamanho do modelo, cerca de 30 vezes menor que o FaceNet. Além disso, o FN8 demonstra alta acurácia na identificação de pessoas sem sacrificar a confiabilidade, medida pela medida F1. Usando uma estratégia de aprendizado com poucos exemplos [40] e imagens em tons de cinza, o FN8 alcançou maior acurácia ao incorporar mais amostras de rosto armazenadas, sem aumentar significativamente o tempo de processamento. Os resultados mostram que o FN8 teve desempenho superior em tempo real, em quadros por segundo (fps), tanto no PC com mais recursos (processador i7-2600) quanto no dispositivo com relativamente poucos recursos (processador N3710). Notavelmente, no PC com mais recursos, o FN8 melhorou a acurácia de reconhecimento de 98,4% (1 amostra) para 99,2% (3 amostras), com aumento desprezível de apenas 0,002 segundo no tempo de processamento.

**[N. T.: pela própria Tabela 3, o FaceNet tem acurácia maior (99,6%) que o FN8 (98,4% e 99,2%); a superioridade do FN8 é em tamanho e velocidade.]**

**Tabela 3.** Comparação de desempenho entre o FN8 e o FaceNet na LFW.

| Modelo | Base de treino, nº de imagens | Função de perda | Tamanho (MB) | Parâmetros (M) | GFlops | Acurácia | F1 | Tempo de inferência (s), CPU i7-2600 | fps | Tempo de inferência (s), CPU N3710 | fps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FaceNet | VGGFace2, 100–200 M | *Triplet* | 95 | 7,5 | 1,6 | 99,6% | – | 0,082 | 12 | 0,840 | 1 |
| FN8 (1 amostra) | CASIA, 0,49 M | Centro + *softmax* | 3,5 | 1,2 | 0,06 | 98,4% | 0,9405 | 0,028 | 35 | 0,220 | 4 |
| FN8 (3 amostras) | CASIA, 0,49 M | Centro + *softmax* | 3,5 | 1,2 | 0,06 | 99,2% | 0,9756 | 0,030 | 33 | 0,232 | 4 |

Além disso, os resultados da Tabela 4 mostram que o modelo leve desenvolvido supera modelos leves de ponta selecionados e variantes leves propostas recentemente em espaço de armazenamento (tamanho do modelo em MB), compacidade (número de parâmetros) e eficiência computacional (GFlops). Entre os três modelos novos, o ELANet alcança a maior acurácia na verificação da LFW, 99,68%; no entanto, ocupa o maior espaço de armazenamento (> 1 M). **[N. T.: a Tabela 4 não informa o tamanho do ELANet em MB; "> 1 M" parece se referir aos 1,6 M de parâmetros.]**

O ConvFaceNeXt, treinado com uma base de tamanho semelhante à do FN8, tem acurácia 0,9% maior que o FN8 na LFW, mas 3,4% menor na AgeDB-30. Já o PocketNetS-256, treinado com a base MS1M-ArcFace, maior (5,8 M), tem o melhor desempenho nas duas bases, mas exige mais que o dobro do tempo de processamento do FN8.

**Tabela 4.** Comparação de desempenho entre o FN8, modelos leves de ponta e outras variantes leves.

| Modelo | Base de treino, nº de imagens | Função de perda | Tamanho (MB) | Parâmetros (M) | GFlops | Acurácia LFW | Acurácia AgeDB-30 | Tempo de inferência (s), CPU i7-11800H | fps |
|---|---|---|---|---|---|---|---|---|---|
| MobileFaceNet [26] | CASIA, 0,49 M | ArcFace | 4 | 0,99 | 0,44 | 99,28% | 93,05% | 0,058 | 17 |
| MobileFaceNets [26] | MS-Celeb-1M limpa, 3,8 M | ArcFace | 4 | 0,99 | 0,44 | 99,55% | 96,07% | – | – |
| MobileFaceNet [5] | MS1M-RetinaFace, 5,1 M | ArcFace | 8,2 | 2,0 | 0,93 | 99,7% | 97,6% | – | – |
| ShuffleFaceNet 1.5x [21] | MS1M-RetinaFace, 5,1 M | ArcFace | 10,5 | 2,6 | 0,58 | 99,67% | 97,3% | 0,043 | 23 |
| VarGFaceNet [27] | MS1M-RetinaFace, 5,1 M | Destilação angular | 20,0 | 5,0 | 1,02 | 99,68% | 97,5% | – | – |
| ELANet [28] | MS1M-RetinaFace, 5,1 M | ArcFace | – | 1,6 | 0,55 | 99,68% | – | 0,073 | 13 |
| PocketNetS-256 [29] | MS1M-ArcFace, 5,8 M | ArcFace | 3,9 | 0,99 | 0,59 | 99,66% | 96,35% | 0,081 | 12 |
| ConvFaceNeXt_PS [30] | UMD, 0,37 M | ArcFace | 4,11 | 0,96 | 0,39 | 99,3% | 92,88% | 0,035 | 28 |
| FN8 (1 amostra) | CASIA, 0,49 M | Centro + *softmax* | 3,5 | 1,2 | 0,06 | 98,4% | 96,26% | 0,033 | 30 |
| FN8 (3 amostras) | CASIA, 0,49 M | Centro + *softmax* | 3,5 | 1,2 | 0,06 | 99,2% | – | 0,035 | 28 |

**[N. T.: na Tabela 4, a referência do VarGFaceNet aparece como [27], mas na Seção 2.2 ele é a referência [25].]**

Apesar de treinado em uma base relativamente pequena (CASIA-WebFace, 0,49 M), o FN8 alcança acurácia competitiva na LFW em comparação com os outros modelos e até supera o MobileFaceNet na AgeDB-30. Isso sugere que a estrutura do FN8, supervisionada em conjunto pela perda de centro e pela perda *softmax*, fornece informação suficiente para uma melhor convergência no treinamento sem sacrificar a generalidade. Isso fica particularmente evidente ao avaliar a eficiência do modelo na AgeDB-30. Como a AgeDB tem apenas uma amostra positiva e uma negativa, os resultados experimentais relatam o FN8 apenas com a estratégia de um exemplo (*one-shot*). Notavelmente, nesse cenário, o FN8 supera o MobileFaceNet treinado na CASIA-WebFace. Nas mesmas condições de teste e de ambiente, o menor tempo de treinamento e a maior velocidade de processamento confirmam a eficácia dos métodos usados no desenvolvimento de um modelo de DL leve.

#### 4.2.2 Comparação de desempenho em cenários de tempo real

Um teste de robustez ambiental examina a robustez do FN8 com amostras de rostos disfarçados. A Figura 10 mostra o resultado do reconhecimento de rostos cadastrados em condições de disfarce, com processamento em tempo real. Essa nova base coletada tem 10 pessoas, com várias imagens estáticas e sequências de vídeo. O modelo, com técnicas de aprendizado com poucos exemplos, reconhece corretamente as identidades em um ambiente interno controlado. O FN8 não só apresentou alta acurácia, como também fez um reconhecimento rápido e robusto diante de imagens de rosto de tamanhos variados, variações de expressão facial e oclusões parciais do rosto. A Figura 11 mostra uma aplicação real dentro de um veículo, com duas pessoas em um carrinho de golfe, para identificação e autorização do motorista com o FN8. Além de fundos complicados, os problemas desafiadores nesse ambiente externo incluem mudanças significativas de iluminação, de pose da cabeça e tremores da câmera causados pela vibração do carrinho em movimento. Usando apenas imagens faciais em tons de cinza, o modelo FN8 supera as interferências do ambiente externo não controlado e reconhece os rostos cadastrados, executando o teste de similaridade para o sistema de identificação e monitoramento do motorista.

> [Figura 10: Reconhecimento em tempo real de rostos disfarçados: (a) os rostos cadastrados; (b) os rostos reconhecidos com sucesso.]
> [Figura 11: Teste de reconhecimento em ambiente externo não controlado, com autorização de acesso a veículos autônomos.]

Para demonstrar a superioridade do FN8 sobre outros modelos leves de reconhecimento facial de ponta, este estudo avaliou seu desempenho em uma pequena base própria, com 12 pessoas e 240 imagens, para treino e teste dos modelos. Escolhemos o ShuffleFaceNet e o MobileFaceNet como modelos de referência e garantimos que todos fossem treinados e validados nas mesmas condições, em um único computador com o mesmo hardware (processador Intel i7, 2,3 GHz, 16 GB de RAM) e a mesma versão de software, sem GPU. A mesma taxa de aprendizado inicial, o mesmo número fixo de épocas e o mesmo número máximo de iterações foram usados para todos os modelos. O conjunto de treino tem 200 imagens, e as 40 restantes foram usadas para teste. Como mostram as Tabelas 5 e 6, o FN8 levou aproximadamente o mesmo tempo que os outros modelos para concluir o treinamento. Notavelmente, apesar do tamanho e do número de parâmetros reduzidos, o FN8 alcançou uma taxa de reconhecimento de 30 fps para uma única identidade, sem sacrificar a acurácia de validação. Isso o torna um candidato ideal para implantação rápida em aplicações de reconhecimento facial em tempo real, como controle de acesso ao vivo em entradas, autorização de motoristas e sistemas de presença em sala de aula. No geral, os resultados experimentais demonstram que o modelo de DL leve desenvolvido supera os modelos leves de ponta selecionados em espaço de armazenamento, compacidade e eficiência computacional, o que o torna mais prático para implantação em aplicações embarcadas.

**Tabela 5.** Comparação do treinamento em uma única CPU com modelos leves de ponta.

| Modelo | Tamanho da imagem | Taxa de aprendizado | Épocas | Tempo decorrido | Iterações | Acurácia de validação |
|---|---|---|---|---|---|---|
| ShuffleFaceNet | 112 × 112 | 0,001 | 30 | 11′37″ | 100 | 100% |
| MobileFaceNet | 112 × 112 | 0,001 | 30 | 14′25″ | 100 | 100% |
| FN8 | 160 × 160 | 0,001 | 30 | 13′19″ | 100 | 100% |

**Tabela 6.** Comparação dos resultados de teste com modelos leves de ponta.

| Modelo | Acurácia | Tempo de inferência (s) | fps |
|---|---|---|---|
| ShuffleFaceNet | 100% | 0,043 | 23 |
| MobileFaceNet | 100% | 0,058 | 17 |
| FN8 | 100% | 0,033 | 30 |

### 4.3 Discussão

#### 4.3.1 Número de dimensões do *embedding*

Este trabalho investiga o tamanho adequado dos *embeddings* por meio de PCA. Aplicando a PCA ao conjunto de treino da LFW, algumas *eigenfaces* características podem ser determinadas e ordenadas pelo grau de variação de cada dimensão. Escolhendo vários tamanhos de *embedding* para o FN8 gerar, a distribuição dos vetores de *embedding* pode ser analisada e comparada. A Figura 12 mostra que o modelo de reconhecimento se confunde facilmente ao distinguir amostras de classes diferentes com vetores de tamanho 128. Com um *embedding* maior, fica mais fácil separar as diferenças entre classes. No entanto, um *embedding* grande demais resulta em uma representação irregular, como mostra a Figura 12c. Conclui-se que o FN8 com *embeddings* de 256 dimensões reconhece melhor as classes de rostos, por isso o tamanho de 256 dimensões foi adotado neste trabalho.

> [Figura 12: Análise por PCA do número de dimensões do *embedding*. Os pontos de cores diferentes representam classes de rostos diferentes. (a) Vetores de tamanho 128. (b) Vetores de tamanho 256. (c) Vetores de tamanho 512.]

#### 4.3.2 Análise de gargalo de desempenho

Esta subseção faz a análise de gargalo de desempenho do modelo de reconhecimento facial proposto, cujo resultado aparece na Figura 13. O eixo horizontal representa os pesos aprendidos em cada nó das camadas, e o eixo vertical mostra o número da iteração na fase de aprendizado. Um modelo de aprendizado saudável se caracteriza por valores espalhados no gráfico a cada iteração. Ao analisar os pesos do FN8, nota-se que eles têm distribuição concentrada nas primeiras 100.000 iterações. À medida que o número de iterações aumenta, a distribuição dos pesos fica mais uniforme. Assim, o FN8 proposto pode ser considerado uma rede saudável e pode ser usado para validar a eficiência dos parâmetros do modelo.

> [Figura 13: Análise de gargalo de desempenho nos pesos das camadas.]

#### 4.3.3 Casos críticos

Este estudo também investiga um desafio crítico para a tarefa de discriminação: gêmeos. Os testes foram feitos com fotos de gêmeos coletadas. As Figuras 14 e 15 mostram os dois pares de gêmeos usados no desafio. A Figura 16 mostra o mapa de similaridade para a discriminação dos gêmeos com o FaceNet e com o FN8, respectivamente. Os resultados mostram que as diferenças entre os dois gêmeos não são suficientes quando as duas pessoas estão na mesma posição; elas são até maiores entre a mesma pessoa em direções diferentes. Analisando os valores, o FN8 com MD como medida de distância tem melhor resolução (faixa de valores) na discriminação. Os resultados revelam seu potencial para distinguir casos críticos, ou até gêmeos não idênticos, aumentando o número de amostras. Embora o FN8 não consiga diferenciar os gêmeos, seu desempenho satisfatório em situações rotineiras ainda mostra alta taxa de discernimento.

> [Figura 14: Gêmeos do sexo masculino: (a) pessoa 1 e (b) pessoa 2.]
> [Figura 15: Gêmeas do sexo feminino: (a) pessoa 1 e (b) pessoa 2.]
> [Figura 16: Mapa de similaridade entre os pares de gêmeos em várias posições: (a) gêmeos masculinos e (b) gêmeas femininas. Entre as imagens aparecem as distâncias medidas pelo FaceNet e pelo FN8, respectivamente.]

#### 4.3.4 Estudo de ablação: efeito das estruturas modificadas

Esta seção investiga o impacto das Inception ResNets refinadas no arcabouço proposto. Como referência, o modelo mantém todas as Inception ResNets (A, B e C) usadas no FaceNet, alcançando acurácia equivalente, de 99%. Para avaliar a importância de cada uma, fizemos experimentos de ablação removendo uma camada de cada vez. Os resultados mostraram que, sem a Inception ResNet A, a acurácia caiu para 86,67%; sem a Inception ResNet B, caiu para 89,25%; e sem a Inception ResNet C, caiu para 92%. Esses resultados sugerem que remover a Inception ResNet C reduz significativamente o tamanho e o número de parâmetros do modelo, com sacrifício pequeno de acurácia, oferecendo um bom compromisso.

Para melhorar ainda mais a taxa de reconhecimento do modelo, foram feitas modificações nas Inception ResNets A e B, para compensar a perda de precisão causada pela redução. Com as estratégias de simplificação citadas aplicadas às Inception ResNets, a acurácia do modelo subiu para 97%. Além disso, ao incorporar às Inception ResNets refinadas um *max-pooling* 2 × 2, o modelo alcançou acurácia de 98,4%. As estruturas simplificadas e refinadas do FN8 permitem o aprendizado com poucos exemplos, atendendo à demanda de desempenho em tempo real. Usando 3 amostras em tons de cinza, o FN8 alcança alta acurácia, de 99,2%. Esses resultados destacam a eficácia das estruturas modificadas em melhorar a acurácia, mantendo a eficiência e atendendo às exigências de desempenho em tempo real.

## 5 Conclusões

Neste estudo, um novo modelo de DL chamado FN8, com arquitetura excepcionalmente leve, foi proposto e testado para reconhecimento facial profundo. Os resultados experimentais mostraram que o modelo proposto superou modelos faciais leves de ponta em acurácia e robustez. A complexidade reduzida do modelo leve proposto o torna particularmente atraente, pela baixa exigência de memória, de apenas 3,5 MB, e pelo pequeno número de parâmetros, ao custo de uma perda muito pequena de acurácia. Usando aprendizado com poucos exemplos a partir de imagens faciais em tons de cinza como entrada para gerar *embeddings* faciais, o FN8 ainda preserva as características faciais fortes para distinguir identidades diferentes e identificar uma não cadastrada. Avaliações experimentais extensas testaram a abordagem proposta em situações complexas e não controladas, o que confirmou a eficácia do modelo. Esse modelo leve de reconhecimento facial é viável para implantação em tempo real em dispositivos com poucos recursos e tem significado prático e potencial de aplicação.

## Contribuições dos autores

Concepção: Z.-Y. Deng, H.-H. Chiang, L.-W. Kang e H.-C. Li. Metodologia: Z.-Y. Deng e H.-H. Chiang. Software: Z.-Y. Deng. Análise e validação: Z.-Y. Deng e H.-C. Li. Investigação: H.-H. Chiang e L.-W. Kang. Recursos: Z.-Y. Deng e L.-W. Kang. Curadoria de dados: H.-H. Chiang, L.-W. Kang e H.-C. Li. Redação do rascunho original: Z.-Y. Deng e H.-C. Li. Redação, revisão e edição: H.-H. Chiang e H.-C. Li. Administração do projeto: H.-H. Chiang e H.-C. Li. Obtenção de financiamento: H.-H. Chiang. Todos os autores leram e concordaram com a versão publicada do manuscrito.

**Declaração de conflito de interesses:** os autores declaram não haver conflito de interesses.

**Disponibilidade dos dados:** os dados que sustentam os resultados deste estudo estão disponíveis com o autor correspondente mediante solicitação razoável.

**Permissão para reproduzir materiais de outras fontes:** nenhuma.

## Referências

As referências estão no idioma original.

1. Schroff, F., Kalenichenko, D., Philbin, J.: FaceNet: A unified embedding for face recognition and clustering. CVPR 2015, pp. 815–823.
2. Li, H.-C., Deng, Z.-Y., Chiang, H.-H.: Lightweight and resource-constrained learning network for face recognition with performance optimization. Sensors 20(21), 6114 (2020). https://doi.org/10.3390/s20216114
3. Zhong, Y., Deng, W., Fang, H., Hu, J., Zhao, D., Li, X., Wen, D.: Dynamic training data dropout for robust deep face recognition. IEEE Trans. Multim. 24, 1186–1197 (2022). https://doi.org/10.1109/TMM.2021.3123478
4. Shi, X., Chai, X., Xie, J., Sun, T.: MC-GCN: A multi-scale contrastive graph convolutional network for unconstrained face recognition with image sets. IEEE Trans. Image Process. 31, 3046–3055 (2022). https://doi.org/10.1109/TIP.2022.3163851
5. Martínez-Díaz, Y. et al.: Benchmarking lightweight face architectures on specific face recognition scenarios. Artif. Intell. Rev. 54, 6201–6244 (2021). https://doi.org/10.1007/s10462-021-09974-2
6. Liu, S. et al.: An identity authentication method combining liveness detection and face recognition. Sensors 19(21), 4733 (2019). https://doi.org/10.3390/s19214733
7. Lee, H. et al.: Face recognition at a distance for a stand-alone access control system. Sensors 20(3), 785 (2020). https://doi.org/10.3390/s20030785
8. Wang, Z. et al.: A new face recognition method for intelligent security. Appl. Sci. 10(3), 852 (2020). https://doi.org/10.3390/app10030852
9. Song, Z. et al.: Spartan face mask detection and facial recognition system. Healthcare 10(1), 87 (2022). https://doi.org/10.3390/healthcare10010087
10. Sun, J., Lu, S.: An improved single shot multibox for video-rate head pose prediction. IEEE Sens. J. 20(20), 12326–12333 (2020). https://doi.org/10.1109/JSEN.2020.2999625
11. Abdi, H., Williams, L.J.: Principle component analysis. Wiley Interdiscip. Rev. Comput. Stat. 2, 433–459 (2010)
12. Lu, J., Plataniotis, K.N., Venetsanopoulos, A.N.: Face recognition using LDA-based algorithms. IEEE Trans. Neural Netw. 14(1), 195–200 (2003). https://doi.org/10.1109/TNN.2002.806647
13. Santaji, G., Ghorpade, J., Shamla, M.: Pattern recognition using neural networks. IJCSIT 2(6), 92–98 (2010)
14. Wang, F. et al.: A novel multi-face recognition method with short training time and lightweight based on ABASNet and H-Softmax. IEEE Access 8, 175370–175384 (2020). https://doi.org/10.1109/ACCESS.2020.3026421
15. Taigman, Y., Yang, M., Ranzato, M., Wolf, L.: DeepFace: Closing the gap to human-level performance in face verification. CVPR 2014, pp. 1701–1708. https://doi.org/10.1109/CVPR.2014.220
16. Sun, Y., Chen, Y., Wang, X., Tang, X.: Deep learning face representation by joint identification-verification. NIPS 2014, vol. 2, pp. 1988–1996.
17. Parkhi, O.M., Vedaldi, A., Zisserman, A.: Deep face recognition. BMVC 2015, pp. 41.1–41.12.
18. Almabdy, S., Elrefaei, L.: Deep convolutional neural network-based approaches for face recognition. Appl. Sci. 9(20), 4397 (2019). https://doi.org/10.3390/app9204397
19. Amos, B., Ludwiczuk, B., Satyanarayanan, M.: OpenFace: A general-purpose face recognition library with mobile applications. CMU School Comp. Sci. 6(2), 20 (2016)
20. Duong, C.N. et al.: MobiFace: A lightweight deep learning face recognition on mobile devices. IEEE BTAS 2019, pp. 1–6. https://doi.org/10.1109/BTAS46853.2019.9185981
21. Martínez-Díaz, Y. et al.: ShuffleFaceNet: A lightweight face architecture for efficient and highly-accurate face recognition. ICCV Workshops 2019.
22. Liu, W. et al.: SphereFace: Deep hypersphere embedding for face recognition. CVPR 2017, pp. 212–220.
23. Wang, H. et al.: CosFace: Large margin cosine loss for deep face recognition. CVPR 2018, pp. 5265–5274.
24. Deng, J., Guo, J., Xue, N., Zafeiriou, S.: ArcFace: Additive angular margin loss for deep face recognition. CVPR 2019, pp. 4690–4699.
25. Yan, M. et al.: VarGFaceNet: An efficient variable group convolutional neural network for lightweight face recognition. ICCV Workshops 2019, pp. 2647–2654. https://doi.org/10.1109/ICCVW.2019.00323
26. Chen, S., Liu, Y., Gao, X., Han, Z.: MobileFaceNets: Efficient CNNs for accurate real-time face verification on mobile devices. CCBR 2018, LNCS 10996. https://doi.org/10.1007/978-3-319-97909-0_46
27. Kocacinar, B. et al.: A real-time CNN-based lightweight mobile masked face recognition system. IEEE Access 10, 63496–63507 (2022). https://doi.org/10.1109/ACCESS.2022.3182055
28. Zhang, P., Zhao, F., Liu, P., Li, M.: Efficient lightweight attention network for face recognition. IEEE Access 10, 31740–31750 (2022). https://doi.org/10.1109/ACCESS.2022.3150862
29. Boutros, F. et al.: PocketNet: Extreme lightweight face recognition network using neural architecture search and multistep knowledge distillation. IEEE Access 10, 46823–46833 (2022). https://doi.org/10.1109/ACCESS.2022.3170561
30. Hoo, S.C., Ibrahim, H., Suandi, S.A.: ConvFaceNeXt: Lightweight networks for face recognition. Mathematics 10(19), 3592 (2022). https://doi.org/10.3390/math10193592
31. Martínez-Díaz, Y. et al.: Towards accurate and lightweight masked face recognition: An experimental evaluation. IEEE Access 10, 7341–7353 (2022). https://doi.org/10.1109/ACCESS.2021.3135255
32. Zhao, G., Yang, H., Yu, M.: Expression recognition method based on a lightweight convolutional neural network. IEEE Access 8, 38528–38537 (2020). https://doi.org/10.1109/ACCESS.2020.2964752
33. Agbo-Ajala, O., Viriri, S.: A lightweight convolutional neural network for real and apparent age estimation in unconstrained face images. IEEE Access 8, 162800–162808 (2020). https://doi.org/10.1109/ACCESS.2020.3022039
34. Wen, Y., Zhang, K., Li, Z., Qiao, Y.: A discriminative feature learning approach for deep face recognition. ECCV 2016, LNCS 9911. https://doi.org/10.1007/978-3-319-46478-7_31
35. Ioffe, S., Szegedy, C.: Batch normalization: Accelerating deep network training by reducing internal covariate shift. ICML 2015, PMLR 37, pp. 448–456.
36. Koch, G., Zemel, R., Salakhutdinov, R.: Siamese neural networks for one-shot image recognition. ICML 2015.
37. Huang, G.B., Ramesh, M., Berg, T., Learned-Miller, E.: Labeled faces in the wild: A database for studying face recognition in unconstrained environments. Technical Report 07-49, University of Massachusetts, Amherst (2007)
38. Moschoglou, S. et al.: AgeDB: The first manually collected, in-the-wild age database. CVPR Workshops 2017, pp. 51–59.
39. Yi, D., Lei, Z., Liao, S., Li, S.Z.: Learning face representation from scratch. arXiv:1411.7923 (2014)
40. Wu, Y., Liu, H., Fu, Y.: Low-shot face recognition with hybrid classifiers. ICCV Workshops 2017, pp. 1933–1939. https://doi.org/10.1109/ICCVW.2017.228

---

## Notas para o TCC

*Seção acrescentada nesta tradução; não faz parte do artigo original.*

- **Por que importa:** é o artigo da pasta que mais se aproxima do problema do TCC em tempo e hardware: mede quadros por segundo em CPUs fracas (Intel N3710, um processador de baixo consumo) e testa um veículo em movimento, com vibração e mudança de luz.
- **Unidade de tempo:** o artigo fala em fps e em segundos por imagem, não em segundos por par, como o benchmark do projeto (item M5 do [documento de lacunas](../lacunas_revisao_bibliografica.md)). Para comparar, use segundos por imagem.
- **Ideias aproveitáveis:** cadastrar mais de uma foto por aluno (com 3 fotos a acurácia na LFW subiu de 98,4% para 99,2%, praticamente sem custo de tempo) e reconhecer sem retreinar quando um aluno novo é cadastrado, o que o sistema já faz com *embeddings*.
- **Cuidado:** os testes em tempo real usam bases próprias de 10 a 12 pessoas, com 100% de acurácia, o que é pouco para conclusões gerais; e o FN8 não está disponível no DeepFace, então não entra direto no benchmark.
