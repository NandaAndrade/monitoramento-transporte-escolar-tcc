# Lacunas da revisão bibliográfica e pontos a rever na comparação entre a literatura e o benchmark

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Data:** 2026-10-05
**Base:** os 8 artigos em `Downloads/Referencias` e o [relatório do benchmark](benchmark_reconhecimento_facial.md).

> Documento de trabalho interno, que não faz parte da monografia. As referências sugeridas ainda precisam ser lidas e aprovadas antes de entrar em `referencias.bib`.
>
> **Legenda:** ✅ = título, autores e veículo confirmados em busca online em 05/10/2026 · ⚠️ = referência clássica citada de memória, que deve ser conferida antes de entrar no `.bib`.

---

## 1. Sugestões de artigos por lacuna

### 1.1 Contexto de aplicação: presença no transporte escolar

| Referência | Por que ler |
|---|---|
| *Student Tracking System in School Bus using Face Recognition and IoT*. In: 7th International Conference on Computing Methodologies and Communication (ICCMC), IEEE, 2023. [IEEE Xplore](https://ieeexplore.ieee.org/document/10084071/) ✅ (autores possivelmente Swathi, S.; Nandhini, A.; Ramya, R., mas isso veio de uma fonte secundária: confira no Xplore) | É o trabalho mais parecido com o seu: câmera na porta do ônibus, Raspberry Pi, GPS e aviso aos pais no embarque e no desembarque. Serve de comparação direta em Trabalhos Relacionados. É um artigo curto de conferência, então use para comparar a arquitetura, não como referência de desempenho. Acesso: IEEE Xplore pelo Portal CAPES (login CAFe/UFMG). |
| *AI-Enabled Wearable IoT Device for Facial Recognition in Student Transportation Systems*. International Journal of Cloud Applications and Computing, v. 16, n. 1, 2026. [ScienceDirect](https://www.sciencedirect.com/org/science/article/pii/S2156183426000057) ✅ | É recente e organiza a arquitetura em camadas (sensoriamento, gateway, servidor, aplicação). Serve de modelo para a Atividade 1.3. |
| *IoT-Based Smart School Bus Security System*. 2023. [ResearchGate](https://www.researchgate.net/publication/370901782) ✅ | Usa **ESP32-CAM** com RFID. É o único trabalho encontrado sobre ESP32 em ônibus escolar e ajuda a justificar o trade-off Raspberry Pi × ESP32. Verifique se foi publicado em periódico ou evento, porque só achamos a versão no ResearchGate. |
| *Student Monitoring System for School Bus Using Facial Recognition*. IEEE, 2019. [IEEE Xplore](https://ieeexplore.ieee.org/document/8862534/) ✅ | Trabalho mais antigo com a mesma proposta. Mostra que o problema já é estudado há alguns anos. |
| SURANTHA, N.; SUGIJAKKO, B. Lightweight face recognition-based portable attendance system with liveness detection. *Internet of Things*, v. 25, 101089, 2024. ✅ | Controle de presença em **Raspberry Pi** com MobileNetV2 e verificação de vivacidade, com 0,6 s por reconhecimento e 96% de acurácia. É a melhor referência de desempenho real em hardware igual ao seu. |
| *LaED: a novel lightweight, edge-aware and explainable deep learning model for privacy-preserving facial attendance tracking in resource-constrained educational environments*. *Scientific Reports*, 2026. [Nature](https://www.nature.com/articles/s41598-026-42051-8) ✅ | Junta presença escolar, borda e **privacidade**, três eixos do seu trabalho. Não conseguimos abrir o texto completo: baixe pelo CAPES. |

### 1.2 Reconhecimento de voz (locutor) embarcado

| Referência | Por que ler |
|---|---|
| DESPLANQUES, B.; THIENPONDT, J.; DEMUYNCK, K. ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification. *Interspeech*, 2020. ⚠️ | Modelo de referência atual em verificação de locutor. Tem o mesmo papel que o ArcFace tem para o rosto. |
| CHEN, T.-W. *et al.* A Lightweight Speaker Verification Model For Edge Device. *APSIPA ASC*, 2023. [IEEE Xplore](https://ieeexplore.ieee.org/document/10317337/) ✅ | Versão leve do ECAPA para dispositivos de borda: 1,31 M de parâmetros e 1,76% de taxa de erro igual (EER) no VoxCeleb1. É o equivalente de voz aos artigos de rosto leves que você já tem. |
| *SPIDER: Lightweight Speaker Identification on Resource-Constrained Embedded Devices*. [PDF](https://www.carloalbertoboano.com/documents/gallacher26spider.pdf) ✅ | Identificação de locutor rodando **no próprio Raspberry Pi** e preservando a privacidade. Confira em qual evento foi publicado. |
| DUFFY, T. P. *Edge Device Speaker Verification*. Dissertação (CUNY). [CUNY Academic Works](https://academicworks.cuny.edu/cc_etds_theses/862/) ✅ | Mostra verificação de locutor em **microcontrolador** com 1 MB de flash e EER ≤ 11%. Ajuda a avaliar se o ESP32 aguentaria a parte de voz. |
| NAGRANI, A.; CHUNG, J. S.; ZISSERMAN, A. VoxCeleb: a large-scale speaker identification dataset. *Interspeech*, 2017. ⚠️ | Base de dados padrão para avaliar voz. Seria o equivalente do LFW se você fizer um benchmark de voz. |

### 1.3 Artigos originais dos modelos testados no benchmark

A banca espera que cada modelo testado seja citado pelo seu artigo original. Hoje nenhum deles está no `referencias.bib`.

| Modelo | Referência original |
|---|---|
| ArcFace | DENG, J. *et al.* ArcFace: Additive Angular Margin Loss for Deep Face Recognition. *CVPR*, 2019. ⚠️ |
| SFace | ZHONG, Y. *et al.* SFace: Sigmoid-Constrained Hypersphere Loss for Robust Face Recognition. *IEEE Transactions on Image Processing*, v. 30, 2021. ⚠️ |
| GhostFaceNet | ALANSARI, M. *et al.* GhostFaceNets: Lightweight Face Recognition Model From Cheap Operations. *IEEE Access*, v. 11, p. 35429–35446, 2023. DOI 10.1109/ACCESS.2023.3266068. ✅ |
| FaceNet / Facenet512 | SCHROFF, F.; KALENICHENKO, D.; PHILBIN, J. FaceNet: A Unified Embedding for Face Recognition and Clustering. *CVPR*, 2015. ✅ (está nas referências do ELANet) |
| VGG-Face | PARKHI, O. M.; VEDALDI, A.; ZISSERMAN, A. Deep Face Recognition. *BMVC*, 2015. ⚠️ |
| DeepFace | TAIGMAN, Y. *et al.* DeepFace: Closing the Gap to Human-Level Performance in Face Verification. *CVPR*, 2014. ⚠️ |
| DeepID | SUN, Y.; WANG, X.; TANG, X. Deep Learning Face Representation from Predicting 10,000 Classes. *CVPR*, 2014. ⚠️ |
| OpenFace | AMOS, B.; LUDWICZUK, B.; SATYANARAYANAN, M. OpenFace: A general-purpose face recognition library with mobile applications. Relatório técnico CMU-CS-16-118, 2016. ⚠️ |
| Dlib | KING, D. E. Dlib-ml: A Machine Learning Toolkit. *Journal of Machine Learning Research*, v. 10, 2009. ⚠️ |
| YuNet (detector) | WU, W.; PENG, H.; YU, S. YuNet: A Tiny Millisecond-level Face Detector. *Machine Intelligence Research*, v. 20, p. 656–665, 2023. DOI 10.1007/s11633-023-1423-y. ✅ |
| RetinaFace (detector) | DENG, J. *et al.* RetinaFace: Single-Shot Multi-Level Face Localisation in the Wild. *CVPR*, 2020. ⚠️ |
| LFW (base) | HUANG, G. B. *et al.* Labeled Faces in the Wild: A Database for Studying Face Recognition in Unconstrained Environments. Relatório técnico 07-49, UMass Amherst, 2007. ⚠️ |
| DeepFace (biblioteca) | SERENGIL, S. I.; ÖZPINAR, A. LightFace: A Hybrid Deep Face Recognition Framework. *ASYU*, 2020. ⚠️ Cite a biblioteca que gerou os números do benchmark. |

### 1.4 Benchmarks comparáveis ao seu

| Referência | Por que ler |
|---|---|
| MARTÍNEZ-DÍAZ, Y. *et al.* Benchmarking lightweight face architectures on specific face recognition scenarios. *Artificial Intelligence Review*, v. 54, p. 6201–6244, 2021. DOI 10.1007/s10462-021-09974-2. ✅ | É o trabalho mais parecido com o seu benchmark: compara modelos leves em vários cenários. Use como referência metodológica e para comparar números. |
| KOLF, J. N. *et al.* EFaR 2023: Efficient Face Recognition Competition. [arXiv](https://arxiv.org/abs/2308.04168) ✅ | Competição de modelos eficientes, com ranking de acurácia por custo computacional. Confira os autores na versão publicada (IJCB 2023). |

### 1.5 Crianças, privacidade e LGPD

| Referência | Por que ler |
|---|---|
| DEB, D.; NAIN, N.; JAIN, A. K. Longitudinal Study of Child Face Recognition. *International Conference on Biometrics (ICB)*, p. 225–232, 2018. [arXiv](https://arxiv.org/abs/1711.03990) ✅ | Mostra que a acurácia cai conforme aumenta o tempo entre o cadastro e o reconhecimento, e que **crianças mais novas são reconhecidas pior**. Justifica recadastrar os alunos periodicamente. Seu benchmark usa só adultos (LFW). |
| *Mitigating Longitudinal Performance Degradation in Child Face Recognition Using Synthetic Data*. 2026. [arXiv](https://arxiv.org/abs/2601.01689) ✅ | Continuação recente do tema. Por enquanto é um preprint no arXiv: veja se já saiu publicado. |
| BRASIL. Lei nº 13.709, de 14 de agosto de 2018 (LGPD), arts. 5º (II), 11 e 14. | Define dado biométrico como dado sensível e exige o melhor interesse da criança. É fonte obrigatória. |
| ANPD. Despacho Decisório nº 2/2026/SFI, Processo nº 00261.007049/2024-06, 4 de agosto de 2026. ✅ | **Muito importante:** a ANPD suspendeu o reconhecimento facial para registro de frequência nas escolas estaduais do Paraná, citando os arts. 6º (X), 11, 14, 23, 46 e 47 da LGPD. É praticamente o seu caso de uso. Tem que ser discutido na monografia, e a arquitetura precisa responder a cada irregularidade apontada. [Resumo na Data Privacy Brasil](https://www.dataprivacybr.org/anpd-suspende-o-uso-de-reconhecimento-facial-em-escolas-publicas-do-parana/); busque o texto oficial no site da ANPD. |

---

## 2. Pontos a rever na comparação entre a literatura e o trabalho

### 2.1 Metodologia do benchmark

- **M1. Protocolo do LFW.** A literatura usa o protocolo oficial: 6.000 pares em 10 partes, com o limiar ajustado em 9 partes e testado na décima. O benchmark usou 384 pares e o limiar padrão do DeepFace. Por isso os números (51–93%) **não podem ser comparados diretamente** com os da literatura (99,0–99,7%). Opções: (a) refazer o teste no protocolo oficial; ou (b) manter os 384 pares e deixar claro no texto que é um protocolo próprio, sem comparar números absolutos.
- **M2. Limiar de decisão.** A precisão de 100% com recall baixo (SFace, GhostFaceNet, FaceNet, OpenFace) indica um limiar conservador demais para este procedimento de teste. Calibre o limiar e reporte também métricas que não dependem dele (curva ROC e EER), como fazem DGFaceNet, ELANet e Jha (2024).
- **M3. Detector e alinhamento.** O Haar sem alinhamento é a explicação mais provável da distância de cerca de 11 pontos entre ArcFace e SFace. Na literatura, essa distância fica abaixo de 0,5 ponto. Refaça com YuNet ou RetinaFace, com alinhamento, antes de concluir qual modelo é melhor. *Atualização (05/10/2026): feito com RetinaFace, com alinhamento — a distância **aumentou** para cerca de 17 pontos (ArcFace 96,61% × SFace 79,69%; ver seção 7 do relatório do benchmark). O detector não explica a diferença; o limiar (M2) passa a ser o suspeito principal. YuNet ainda não testado.*
- **M4. Hardware do teste de tempo.** Os tempos foram medidos no PC, não no Raspberry Pi com Hailo. Os artigos medem no próprio dispositivo (Lv: Raspberry Pi, NCS e TX2; DGFaceNet: embarcado; Surantha: Raspberry Pi). Ou meça no hardware real, ou deixe claro que os tempos são relativos entre os modelos.
- **M5. Tempo por par × por quadro.** O relatório mede segundos por par (dois rostos). A literatura costuma usar milissegundos por imagem ou quadros por segundo (FN8). Converta, ou explique a unidade.
- **M6. Amostra.** Com 96 pessoas e 384 pares, uma diferença de 1 ponto vale cerca de 4 pares. Informe o intervalo de confiança ou o desvio entre as 10 partes antes de afirmar que um modelo é melhor que outro.
- **M7. Base parecida com o uso real.** O LFW tem adultos famosos, fotos de boa qualidade, sem vibração nem contraluz. Planeje um teste extra com crianças e condições de ônibus (base própria com consentimento, ou base pública de crianças), em linha com Deb, Nain e Jain (2018).

### 2.2 Interpretação e escrita

- **E1. O que é "ArcFace".** Na literatura, ArcFace é uma *técnica de treinamento* (função de perda). O que foi testado é a ResNet treinada com ArcFace da biblioteca DeepFace. GhostFaceNet, MobileFaceNet e ELANet também são treinados com ArcFace. Escreva "ResNet treinada com ArcFace (implementação DeepFace)" para não comparar coisas diferentes.
- **E2. Qual GhostFaceNet.** O DGFaceNet compara com um "GhostFaceNet (Zhao *et al.*, 2023)", do mesmo grupo. O modelo da biblioteca DeepFace é o de Alansari *et al.* (2023). Não use o 99,60% do DGFaceNet como valor de referência para o modelo que você testou sem confirmar qual é.
- **E3. Números dos artigos clássicos.** Elngar e Kayed (98,2%, Haar + PCA) e Meddeb *et al.* (93%, LBPH) testaram em bases pequenas e controladas (ORL e bases próprias com até 20 pessoas). Não use esses valores para dizer que os métodos clássicos se igualam ao deep learning.
- **E4. Versão do Lv *et al.* (2021).** O PDF é a versão *pre-proof*. Confira os números finais na versão publicada (DOI 10.1016/j.micpro.2021.104034) e apague o PDF duplicado da pasta.
- **E5. Contribuição do isolamento por processo.** Nenhum dos 8 artigos fala da distorção de tempo causada por vários modelos carregados no mesmo processo. Apresente isso como uma contribuição metodológica, explicando o problema e a correção.
- **E6. Ligar ao requisito de 90%.** A meta do projeto é acurácia acima de 90%. Com o detector Haar, só o ArcFace passa disso; com o RetinaFace, o VGG-Face também passa (95,57%). O procedimento de teste ainda desfavorece os demais (M1 e M2). Não descarte SFace e GhostFaceNet antes de refazer o teste.
- **E7. Fusão voz + rosto.** O Jha (2024) junta as duas modalidades no nível das características e não roda em hardware embarcado. Defina se o seu sistema vai juntar as *características* (como Jha) ou as *decisões* de cada modelo, que é mais simples de embarcar, e justifique com essa referência.
- **E8. Verificação de vivacidade.** Jha (2024) e Surantha e Sugijakko (2024) incluem proteção contra fotos e gravações. Decida se isso entra no escopo ou se fica como limitação declarada.

### 2.3 Arquitetura e requisitos

- **A1. Borda × nuvem.** Sajjad *et al.* (2020) faz a detecção no Raspberry Pi e a classificação na nuvem. Com internet instável no meio rural, justifique por que o seu reconhecimento acontece no próprio ônibus, com sincronização posterior.
- **A2. ESP32.** Nenhum dos 8 artigos testa ESP32. Use o *IoT-Based Smart School Bus Security System* (ESP32-CAM) e a dissertação de Duffy (voz em microcontrolador) para fechar o trade-off com dados, e não só com argumentos.
- **A3. LGPD diante do caso do Paraná.** Para cada irregularidade apontada pela ANPD (base legal, proporcionalidade, segurança, melhor interesse da criança, transparência), registre nos requisitos qual medida o sistema adota. Exemplos: processamento local, guardar só os embeddings e não as fotos, retenção mínima, alternativa sem biometria para quem não consentir.

---

## 3. Próximos passos sugeridos

1. Baixar pelo Portal CAPES os artigos marcados como de alta relevância na Seção 1 e conferir os itens ⚠️.
2. Refazer o benchmark atendendo M1–M3 (protocolo oficial, limiar calibrado, YuNet ou RetinaFace com alinhamento). *M3 feito em parte: RetinaFace com alinhamento testado; falta YuNet, M1 e M2.*
3. Só depois de ler e aprovar cada artigo, incluí-lo no `referencias.bib` e na revisão bibliográfica da monografia.
