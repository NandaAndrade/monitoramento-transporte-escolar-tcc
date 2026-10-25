# Leituras: traduções e guias dos artigos de referência

Material de estudo em português dos 30 artigos da pasta `docs/Referencias`. Cada arquivo tem o mesmo nome do PDF correspondente.

Há dois tipos de documento:

- **Tradução integral:** só para os 4 artigos publicados com licença aberta Creative Commons Atribuição (CC BY), que permite traduzir e redistribuir com crédito aos autores. Cada tradução traz a licença, o crédito e as notas da tradução marcadas como **[N. T.]**.
- **Guia de leitura:** para os 26 artigos protegidos por direitos autorais, que não podem ser traduzidos na íntegra. O guia explica o problema, a ideia central, os resultados principais, as limitações e a ligação com o TCC, com outras palavras, e termina com perguntas para conferir a leitura. Ele ajuda a ler o original, mas não o substitui; para citar números, confira sempre no PDF.

Todos os documentos terminam com a ligação do artigo com o TCC.

## Traduções integrais (CC BY)

| Arquivo | Artigo | Tema |
|---|---|---|
| [elngar_2020_seguranca_veicular_reconhecimento_facial_iot.md](elngar_2020_seguranca_veicular_reconhecimento_facial_iot.md) | Elngar e Kayed, *Open Computer Science*, 2020 | Segurança veicular com Raspberry Pi, Haar e PCA |
| [jha_2024_presenca_biometria_rosto_e_voz.md](jha_2024_presenca_biometria_rosto_e_voz.md) | Jha, Jain e Srivastava, *AIP Advances*, 2024 | Presença com fusão de rosto e voz e detecção de vivacidade |
| [zhang_2022_elanet.md](zhang_2022_elanet.md) | Zhang *et al.*, *IEEE Access*, 2022 | ELANet, rede leve com atenção (tabelas no PDF) |
| [deng_2023_modelo_leve_reconhecimento_facial_tempo_real.md](deng_2023_modelo_leve_reconhecimento_facial_tempo_real.md) | Deng *et al.*, *IET Image Processing*, 2023 | FN8, versão encolhida do FaceNet, tempo real em CPU fraca |

## Guias de leitura

### Métodos clássicos e bases de dados

| Arquivo | Artigo | Citado na Visão Geral |
|---|---|---|
| [turk_1991_eigenfaces.md](turk_1991_eigenfaces.md) | Turk e Pentland, 1991: Eigenfaces | Sim |
| [belhumeur_1997_eigenfaces_vs_fisherfaces.md](belhumeur_1997_eigenfaces_vs_fisherfaces.md) | Belhumeur *et al.*, 1997: Fisherfaces | Sim |
| [samaria_1994_base_att_orl.md](samaria_1994_base_att_orl.md) | Samaria e Harter, 1994: base AT&T/ORL | Sim |
| [ahonen_2004_lbph_local_binary_patterns.md](ahonen_2004_lbph_local_binary_patterns.md) | Ahonen *et al.*, 2004: LBPH | Sim |
| [huang_2007_base_lfw.md](huang_2007_base_lfw.md) | Huang *et al.*, 2007: base LFW | Sim |

### Modelos, detectores e ferramenta do benchmark

| Arquivo | Artigo | Citado na Visão Geral |
|---|---|---|
| [schroff_2015_facenet.md](schroff_2015_facenet.md) | Schroff *et al.*, 2015: FaceNet | Sim |
| [deng_2019_arcface.md](deng_2019_arcface.md) | Deng *et al.*, 2019: ArcFace | Sim |
| [zhong_2021_sface.md](zhong_2021_sface.md) | Zhong *et al.*, 2021: SFace | Sim |
| [deng_2020_retinaface.md](deng_2020_retinaface.md) | Deng *et al.*, 2020: RetinaFace | Sim |
| [wu_2023_yunet.md](wu_2023_yunet.md) | Wu *et al.*, 2023: YuNet | Sim |
| [serengil_2020_lightface_biblioteca_deepface.md](serengil_2020_lightface_biblioteca_deepface.md) | Serengil e Ozpinar, 2020: biblioteca DeepFace | Sim |
| [parkhi_2015_vgg_face.md](parkhi_2015_vgg_face.md) | Parkhi *et al.*, 2015: VGG-Face | Sim |
| [taigman_2014_deepface.md](taigman_2014_deepface.md) | Taigman *et al.*, 2014: modelo DeepFace (Facebook) | Sim |
| [sun_2014_deepid.md](sun_2014_deepid.md) | Sun *et al.*, 2014: DeepID | Sim |
| [amos_2016_openface.md](amos_2016_openface.md) | Amos *et al.*, 2016: OpenFace (Carnegie Mellon) | Sim |
| [king_2009_dlib_ml.md](king_2009_dlib_ml.md) | King, 2009: biblioteca Dlib-ml | Sim |
| [alansari_2023_ghostfacenets.md](alansari_2023_ghostfacenets.md) | Alansari *et al.*, 2023: GhostFaceNets | Sim |
| [viola_2001_haar_cascade.md](viola_2001_haar_cascade.md) | Viola e Jones, 2001: Haar Cascade (detector do OpenCV) | Sim |

### Aplicações embarcadas e trabalhos correlatos

| Arquivo | Artigo | Citado na Visão Geral |
|---|---|---|
| [lv_2021_reconhecimento_facial_sistemas_embarcados.md](lv_2021_reconhecimento_facial_sistemas_embarcados.md) | Lv *et al.*, 2021: reconhecimento em sistemas embarcados | Não |
| [meddeb_2023_robo_vigilancia_raspberry_pi_iot.md](meddeb_2023_robo_vigilancia_raspberry_pi_iot.md) | Meddeb *et al.*, 2023: robô de vigilância com Raspberry Pi | Não |
| [sajjad_2020_raspberry_pi_reconhecimento_facial_cidades.md](sajjad_2020_raspberry_pi_reconhecimento_facial_cidades.md) | Sajjad *et al.*, 2020: Raspberry Pi e nuvem | Não |
| [zhao_2023_dgfacenet.md](zhao_2023_dgfacenet.md) | Zhao *et al.*, 2023: DGFaceNet | Não |
| [garg_2021_onibus_escolar_inteligente_iot.md](garg_2021_onibus_escolar_inteligente_iot.md) | Garg *et al.*, 2021: ônibus escolar com RFID e ESP32-CAM | Candidata (`% CITAR:`) |
| [duarte_2025_classic_chamada_escolar_iot_borda.md](duarte_2025_classic_chamada_escolar_iot_borda.md) | Duarte *et al.*, 2025: CLASSIC, chamada escolar com Raspberry Pi, DeepFace e borda | Sim |

### Reconhecimento de voz

| Arquivo | Artigo | Citado na Visão Geral |
|---|---|---|
| [desplanques_2020_ecapa_tdnn_verificacao_locutor.md](desplanques_2020_ecapa_tdnn_verificacao_locutor.md) | Desplanques *et al.*, 2020: ECAPA-TDNN | Sim |
| [nagrani_2017_base_voxceleb.md](nagrani_2017_base_voxceleb.md) | Nagrani *et al.*, 2017: base VoxCeleb | Sim |

## Ordem de leitura sugerida

1. **Base do benchmark:** LFW → DeepFace (LightFace) → FaceNet → ArcFace → SFace.
2. **Outros modelos do benchmark:** DeepFace (Taigman) → DeepID → VGG-Face → OpenFace → Dlib-ml → GhostFaceNets.
3. **Detecção:** Haar Cascade (Viola e Jones) → RetinaFace → YuNet.
4. **Hardware e aplicações:** Deng 2023 (FN8) → Lv 2021 → Garg 2021 → Meddeb 2023 → Sajjad 2020.
5. **Redes leves:** ELANet → DGFaceNet.
6. **Voz e vivacidade:** VoxCeleb → ECAPA-TDNN → Jha 2024.
7. **Histórico, para a revisão bibliográfica:** Eigenfaces → Fisherfaces → AT&T → LBPH → Elngar 2020.

## Avisos

- Os guias de Belhumeur (1997) e Samaria (1994) foram escritos sem conferir os números no PDF, porque o texto desses arquivos não pôde ser extraído. Os do Sajjad (2020) também têm detalhes não conferidos.
- Nas traduções do Elngar, do Jha e do Deng 2023, há inconsistências do próprio original (tabelas que não somam 100%, números de referência trocados), sinalizadas com **[N. T.]**.
- O guia do Dlib-ml (King, 2009) trata da biblioteca: o artigo não descreve a rede de reconhecimento facial usada no benchmark.
