# Referências da Visão Geral: citação e resumo

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Data:** 2026-10-18
**Base:** as 13 entradas de [referencias.bib](../monografia/referencias.bib), todas citadas em [visao_geral.tex](../monografia/visao_geral.tex).

> Documento de estudo interno, que não faz parte dos entregáveis. Os links de DOI foram conferidos em 18/10/2026 e levam à página do editor; os artigos da IEEE, Springer e Elsevier costumam pedir login, então acesse pelo [Portal de Periódicos CAPES](https://www.periodicos.capes.gov.br/) (login CAFe/UFMG) ou use a versão aberta do arXiv, quando indicada. Os resumos foram escritos a partir do conteúdo conhecido de cada trabalho, **não de uma leitura dos PDFs nesta data**. Os números citados (acurácias, tamanhos de base) devem ser conferidos no original antes de entrarem na monografia, junto com os metadados marcados `% CONFERIR` no `.bib`.

---

## 1. Métodos clássicos de reconhecimento facial

### 1.1 Eigenfaces

TURK, M.; PENTLAND, A. Eigenfaces for recognition. **Journal of Cognitive Neuroscience**, v. 3, n. 1, p. 71–86, 1991. Chave: `turk1991eigenfaces`.

**Acesso:** [DOI 10.1162/jocn.1991.3.1.71](https://doi.org/10.1162/jocn.1991.3.1.71)

**Resumo.** Trata cada imagem de rosto como um vetor e aplica a análise de componentes principais (PCA) a um conjunto de treino. Os autovetores principais, chamados de *eigenfaces*, formam um "espaço de rostos" de poucas dimensões. Cada rosto é representado pelos seus pesos nesse espaço, e o reconhecimento consiste em achar a pessoa cadastrada com os pesos mais próximos. O método é simples e rápido, mas a PCA guarda as direções de maior variância, que muitas vezes vêm da iluminação e não da identidade. Por isso o desempenho cai bastante com mudanças de luz, de pose e de expressão.

**Uso no projeto.** Marco histórico na revisão bibliográfica; justifica por que métodos clássicos não servem para o interior do ônibus.

### 1.2 Fisherfaces

BELHUMEUR, P. N.; HESPANHA, J. P.; KRIEGMAN, D. J. Eigenfaces vs. Fisherfaces: recognition using class specific linear projection. **IEEE Transactions on Pattern Analysis and Machine Intelligence**, v. 19, n. 7, p. 711–720, 1997. Chave: `belhumeur1997eigenfaces`.

**Acesso:** [DOI 10.1109/34.598228](https://doi.org/10.1109/34.598228)

**Resumo.** Propõe o Fisherfaces, que troca a PCA pela análise discriminante linear de Fisher (LDA). Em vez de guardar as direções de maior variância, a LDA busca as que maximizam a separação entre pessoas diferentes e minimizam a variação entre fotos da mesma pessoa. Antes da LDA, aplica-se uma PCA para evitar matrizes singulares. Nos experimentos com variação de iluminação e expressão, o Fisherfaces teve taxas de erro bem menores que o Eigenfaces.

**Uso no projeto.** Marco histórico, junto com o Eigenfaces.

### 1.3 LBPH (Local Binary Patterns)

AHONEN, T.; HADID, A.; PIETIKÄINEN, M. Face recognition with local binary patterns. In: COMPUTER VISION – ECCV 2004. Berlin: Springer, 2004. p. 469–481. (Lecture Notes in Computer Science, v. 3021). Chave: `ahonen2004face`.

**Acesso:** [DOI 10.1007/978-3-540-24670-1_36](https://doi.org/10.1007/978-3-540-24670-1_36)

**Resumo.** Descreve o rosto pela sua textura. A imagem é dividida em regiões; em cada uma, cada pixel recebe um código binário que compara sua intensidade com a dos vizinhos (padrão binário local), e os códigos são resumidos em um histograma. Os histogramas das regiões são concatenados em um único descritor, e dois rostos são comparados por uma distância qui-quadrado ponderada, com mais peso para regiões como olhos e boca. Na base FERET, o método superou a PCA e outros métodos da época, e é menos sensível a variações uniformes de iluminação.

**Uso no projeto.** Marco histórico; o LBPH ainda aparece em sistemas de presença de baixo custo, e serve de contraste com os modelos profundos.

---

## 2. Reconhecimento facial com aprendizado profundo

### 2.1 FaceNet

SCHROFF, F.; KALENICHENKO, D.; PHILBIN, J. FaceNet: a unified embedding for face recognition and clustering. In: IEEE CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION (CVPR), 2015. **Proceedings** [...]. 2015. p. 815–823. Chave: `schroff2015facenet`.

**Acesso:** [DOI 10.1109/CVPR.2015.7298682](https://doi.org/10.1109/CVPR.2015.7298682) · versão aberta: [arXiv 1503.03832](https://arxiv.org/abs/1503.03832)

**Resumo.** Treina uma rede convolucional para mapear cada rosto diretamente em um vetor de 128 dimensões (*embedding*), em que a distância euclidiana mede a semelhança entre rostos. O treino usa a *triplet loss*: para cada trio (âncora, mesma pessoa, outra pessoa), a rede é penalizada se a âncora não estiver mais perto da mesma pessoa do que da outra, com uma margem. Os autores mostram que a escolha de trios difíceis é essencial para a convergência. Um mesmo *embedding* serve para verificação, identificação e agrupamento. Obteve 99,63% de acurácia na LFW.

**Uso no projeto.** Base conceitual dos *embeddings*; os modelos Facenet e Facenet512 do benchmark derivam dele.

### 2.2 ArcFace

DENG, J.; GUO, J.; XUE, N.; ZAFEIRIOU, S. ArcFace: additive angular margin loss for deep face recognition. In: IEEE/CVF CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION (CVPR), 2019. **Proceedings** [...]. 2019. p. 4690–4699. Chave: `deng2019arcface`.

**Acesso:** [DOI 10.1109/CVPR.2019.00482](https://doi.org/10.1109/CVPR.2019.00482) · versão aberta: [arXiv 1801.07698](https://arxiv.org/abs/1801.07698)

**Resumo.** Propõe uma função de perda para treinar redes de reconhecimento facial. Os *embeddings* e os pesos de cada classe são normalizados sobre uma hiperesfera, e a perda soma uma margem fixa ao ângulo entre o *embedding* e o centro da sua classe. Isso obriga a rede a deixar fotos da mesma pessoa muito mais próximas (em ângulo) do que de outras pessoas, e a margem tem interpretação geométrica direta (distância geodésica na esfera). Com uma ResNet treinada com essa perda, os autores chegaram a resultados de referência em várias bases, acima de 99,8% na LFW.

**Uso no projeto.** Melhor modelo do benchmark (96,61% com RetinaFace). Lembrete do [doc de lacunas](lacunas_revisao_bibliografica.md) (item E1): ArcFace é a função de perda; o que foi testado é a ResNet treinada com ArcFace da biblioteca DeepFace.

### 2.3 SFace

ZHONG, Y.; DENG, W.; HU, J.; ZHAO, D.; LI, X.; WEN, D. SFace: sigmoid-constrained hypersphere loss for robust face recognition. **IEEE Transactions on Image Processing**, v. 30, p. 2587–2598, 2021. Chave: `zhong2021sface`.

**Acesso:** [DOI 10.1109/TIP.2020.3048632](https://doi.org/10.1109/TIP.2020.3048632) · versão aberta: [arXiv 2205.12010](https://arxiv.org/abs/2205.12010)

**Resumo.** Parte da observação de que perdas com margem, como a ArcFace, forçam demais a separação e acabam se ajustando a rótulos errados e a imagens de baixa qualidade das bases de treino. A SFace também trabalha na hiperesfera, mas controla separadamente a aproximação de fotos da mesma pessoa e o afastamento de pessoas diferentes por duas curvas sigmoides, que reduzem o "empurrão" quando a amostra já está bem posicionada. O resultado é um treino mais moderado e mais robusto a ruído. O modelo é leve e tem versão oficial no OpenCV.

**Uso no projeto.** Candidato leve: o mais rápido e o menor do benchmark (5 MB, 0,04 s de reconhecimento por par), mas abaixo de 82% de acurácia com o limiar padrão.

---

## 3. Detecção facial

### 3.1 RetinaFace

DENG, J.; GUO, J.; VERVERAS, E.; KOTSIA, I.; ZAFEIRIOU, S. RetinaFace: single-shot multi-level face localisation in the wild. In: IEEE/CVF CONFERENCE ON COMPUTER VISION AND PATTERN RECOGNITION (CVPR), 2020. **Proceedings** [...]. 2020. p. 5203–5212. Chave: `deng2020retinaface`.

**Acesso:** [DOI 10.1109/CVPR42600.2020.00525](https://doi.org/10.1109/CVPR42600.2020.00525) · versão aberta: [arXiv 1905.00641](https://arxiv.org/abs/1905.00641) (título da versão do arXiv: *Single-stage Dense Face Localisation in the Wild*)

**Resumo.** Detector de rosto de estágio único que, além da caixa do rosto, prevê cinco pontos de referência (olhos, nariz e cantos da boca) e uma malha 3D densa do rosto, aprendida de forma auto-supervisionada. Usa uma pirâmide de características para encontrar rostos de tamanhos muito diferentes na mesma imagem. Os autores anotaram os cinco pontos na base WIDER FACE e mostraram que essa supervisão extra melhora a detecção, sobretudo nos rostos difíceis (pequenos, parcialmente cobertos ou de lado). Os pontos de referência também permitem alinhar o rosto antes do reconhecimento.

**Uso no projeto.** Detector que mais melhorou o benchmark (ArcFace de 92,97% para 96,61%), mas custa cerca de 0,6 s por imagem na CPU.

### 3.2 YuNet

WU, W.; PENG, H.; YU, S. YuNet: a tiny millisecond-level face detector. **Machine Intelligence Research**, v. 20, n. 5, p. 656–665, 2023. Chave: `wu2023yunet`.

**Acesso:** [DOI 10.1007/s11633-023-1423-y](https://doi.org/10.1007/s11633-023-1423-y)

**Resumo.** Detector de rosto projetado para dispositivos com poucos recursos. Tem cerca de 75 mil parâmetros, usa uma rede de base muito enxuta e uma cabeça de detecção sem âncoras, e roda em poucos milissegundos por imagem em CPU. Na WIDER FACE, alcança acurácia competitiva com detectores muito maiores, ficando atrás deles principalmente nos rostos difíceis. Está integrado ao OpenCV (`FaceDetectorYN`), o que facilita o uso no Raspberry Pi.

**Uso no projeto.** Próximo detector a testar no benchmark: pode chegar perto do RetinaFace com custo muito menor.

---

## 4. Bases de dados e ferramenta de avaliação

### 4.1 LFW

HUANG, G. B.; RAMESH, M.; BERG, T.; LEARNED-MILLER, E. **Labeled Faces in the Wild**: a database for studying face recognition in unconstrained environments. Amherst: University of Massachusetts, 2007. (Technical Report 07-49). Chave: `huang2007lfw`.

**Acesso:** [site KAGGLE da LFW](https://www.kaggle.com/datasets/jessicali9530/lfw-dataset) e [relatório técnico em PDF](https://people.cs.umass.edu/~elm/papers/lfw.pdf) 

**Resumo.** Base com 13.233 fotos de 5.749 pessoas públicas, coletadas da internet, com variação natural de pose, iluminação, expressão e fundo. Foi criada para a tarefa de verificação: dizer se duas fotos são da mesma pessoa. O protocolo oficial usa 6.000 pares divididos em 10 partes, com validação cruzada. Tornou-se a base padrão de comparação da área, embora hoje os modelos modernos já passem de 99% nela.

**Uso no projeto.** Base do benchmark (96 pessoas, 384 pares). Atenção ao item M1 do [doc de lacunas](lacunas_revisao_bibliografica.md): o protocolo usado é próprio, então os números não se comparam diretamente com os da literatura.

### 4.2 AT&T / Olivetti (ORL)

SAMARIA, F. S.; HARTER, A. C. Parameterisation of a stochastic model for human face identification. In: IEEE WORKSHOP ON APPLICATIONS OF COMPUTER VISION, 1994. **Proceedings** [...]. 1994. p. 138–142. Chave: `samaria1994att`.

**Acesso:** [DOI 10.1109/ACV.1994.341300](https://doi.org/10.1109/ACV.1994.341300)

**Resumo.** O artigo propõe identificar rostos com modelos ocultos de Markov e estuda como escolher os parâmetros desse modelo. Para os experimentos, os autores montaram no Olivetti Research Laboratory, em Cambridge, a base hoje conhecida como ORL ou AT&T: 40 pessoas com 10 fotos cada, em tons de cinza, com pequenas variações de pose, expressão e acessórios, sobre fundo uniforme. É a citação usual para quem usa a base.

**Uso no projeto.** Segunda base pública preparada em `pesquisa/dados/att/`; condições controladas, útil como contraste com a LFW.

### 4.3 DeepFace / LightFace

SERENGIL, S. I.; OZPINAR, A. LightFace: a hybrid deep face recognition framework. In: INNOVATIONS IN INTELLIGENT SYSTEMS AND APPLICATIONS CONFERENCE (ASYU), 2020. **Proceedings** [...]. IEEE, 2020. p. 23–27. Chave: `serengil2020lightface`.

**Acesso:** [DOI 10.1109/ASYU50717.2020.9259802](https://doi.org/10.1109/ASYU50717.2020.9259802) · biblioteca: [github.com/serengil/deepface](https://github.com/serengil/deepface)

**Resumo.** Apresenta a biblioteca Python hoje chamada DeepFace, que reúne vários modelos de reconhecimento facial pré-treinados (VGG-Face, FaceNet, OpenFace, DeepFace do Facebook, DeepID, ArcFace, Dlib, entre outros) atrás de uma mesma interface. A biblioteca executa todas as etapas (detecção, alinhamento, representação e verificação) com poucos comandos, e os autores comparam o desempenho dos modelos nesse pipeline comum.

**Uso no projeto.** Ferramenta que gerou todos os números do benchmark; deve ser citada sempre que os resultados aparecerem.

---

## 5. Comunicação e legislação

### 5.1 MQTT 5.0

OASIS. **MQTT Version 5.0**. OASIS Standard, 2019. Disponível em: <https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html>. Chave: `oasis2019mqtt`.

**Acesso:** [especificação MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)

**Resumo.** Especificação oficial do protocolo MQTT, de mensagens por publicação e assinatura: os dispositivos publicam mensagens em tópicos, um servidor intermediário (*broker*) as recebe e as repassa a quem assinou aquele tópico. O cabeçalho é pequeno e a conexão é mantida aberta, o que o torna adequado a redes lentas ou instáveis. Define três níveis de qualidade de serviço: QoS 0 (no máximo uma entrega), QoS 1 (pelo menos uma entrega, com confirmação) e QoS 2 (exatamente uma entrega). A versão 5.0 acrescenta códigos de motivo nas respostas, expiração de sessão e de mensagens e propriedades definidas pelo usuário.

**Uso no projeto.** Meio de envio dos eventos. O sistema usa QoS 1 e um UUID por evento: a entrega "pelo menos uma vez" pode duplicar, e o UUID permite descartar duplicatas (RF-08).

### 5.2 LGPD

BRASIL. **Lei nº 13.709, de 14 de agosto de 2018**. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, 2018. Disponível em: <https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm>. Chave: `brasil2018lgpd`.

**Acesso:** [texto da lei no Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

**Resumo.** Regula o tratamento de dados pessoais no Brasil. Os pontos mais relevantes para o projeto são: o art. 5º, II, que classifica o dado biométrico como dado pessoal sensível; o art. 6º, com os princípios de finalidade, necessidade (minimização) e segurança; o art. 11, que restringe as hipóteses de tratamento de dados sensíveis; o art. 14, que exige que o tratamento de dados de crianças e adolescentes seja feito no seu melhor interesse e, para crianças, com consentimento específico de pelo menos um dos pais ou responsável; e o art. 46, que obriga a adotar medidas de segurança.

**Uso no projeto.** Fundamenta não guardar imagem nem áudio (RF-05, RNF-07), o consentimento registrado antes do cadastro (RF-21) e a retenção mínima (RNF-16). Será detalhada na Atividade 1.4, junto com a decisão da ANPD sobre as escolas do Paraná (ver [doc de lacunas](lacunas_revisao_bibliografica.md), seção 1.5).

---

## 6. Referências candidatas, ainda não citadas

Estão indicadas em comentários `% CITAR:` no [visao_geral.tex](../monografia/visao_geral.tex) e entram no `.bib` só depois de lidas. Detalhes e links no [doc de lacunas](lacunas_revisao_bibliografica.md), seções 1.1 e 1.2.

| Referência | Assunto | Acesso |
|---|---|---|
| DESPLANQUES, B.; THIENPONDT, J.; DEMUYNCK, K. ECAPA-TDNN. *Interspeech*, 2020. | Modelo de referência em verificação de locutor | [arXiv 2005.07143](https://arxiv.org/abs/2005.07143) |
| CHEN, T.-W. *et al.* A Lightweight Speaker Verification Model for Edge Device. *APSIPA ASC*, 2023. | Verificação de locutor leve, em borda | [IEEE Xplore](https://ieeexplore.ieee.org/document/10317337/) |
| NAGRANI, A.; CHUNG, J. S.; ZISSERMAN, A. VoxCeleb. *Interspeech*, 2017. | Base padrão de avaliação de voz | [arXiv 1706.08612](https://arxiv.org/abs/1706.08612) |
| *Student Tracking System in School Bus using Face Recognition and IoT*. ICCMC, IEEE, 2023. | Trabalho correlato: câmera na porta do ônibus com Raspberry Pi | [IEEE Xplore](https://ieeexplore.ieee.org/document/10084071/) |
| *IoT-Based Smart School Bus Security System*. 2023. | Trabalho correlato: ESP32-CAM com RFID | [ResearchGate](https://www.researchgate.net/publication/370901782) |
| *Student Monitoring System for School Bus Using Facial Recognition*. IEEE, 2019. | Trabalho correlato mais antigo | [IEEE Xplore](https://ieeexplore.ieee.org/document/8862534/) |
| SURANTHA, N.; SUGIJAKKO, B. *Internet of Things*, v. 25, 101089, 2024. | Presença por reconhecimento facial em Raspberry Pi | [DOI 10.1016/j.iot.2024.101089](https://doi.org/10.1016/j.iot.2024.101089) |
