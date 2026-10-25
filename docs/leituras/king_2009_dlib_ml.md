# Guia de leitura: Dlib-ml, biblioteca de aprendizado de máquina em C++ (King, 2009)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta para o texto (a licença Boost é do código), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** KING, D. E. Dlib-ml: A Machine Learning Toolkit. *Journal of Machine Learning Research*, v. 10, p. 1755–1758, 2009.
> **PDF local:** `docs/Referencias/king_2009_dlib_ml.pdf` · **Chave no .bib:** `king2009dlib`

---

## Em uma frase

Artigo curto (4 páginas) que apresenta a Dlib-ml, uma biblioteca de código aberto em C++ com álgebra linear e algoritmos de aprendizado de máquina baseados em *kernels*.

## Atenção: o que este artigo **não** contém

O artigo descreve a **biblioteca**, não a rede de reconhecimento facial. O modelo "Dlib" do benchmark é uma rede treinada depois pelo próprio autor, com a biblioteca dlib, e documentada só no site do projeto (essa informação vem da documentação do dlib, não deste artigo). Não há nenhum resultado de reconhecimento facial neste artigo. Cita-se o artigo porque é a referência formal da biblioteca; o modelo em si deve ser descrito no texto, de preferência com uma nota.

## O que o artigo apresenta

1. **Objetivo:** oferecer em C++ um ambiente parecido com o que já existia em Python, R e Matlab para desenvolver aprendizado de máquina.
2. **Projeto do software:** componentes independentes, com documentação extensa e um modo de depuração que confere contratos (pré e pós-condições) de cada função.
3. **Álgebra linear:** expressões parecidas com as do Matlab que, compiladas, ficam quase tão rápidas quanto código C otimizado, e usam a BLAS quando disponível.
4. **Algoritmos com *kernels*:** SVM (incluindo uma reimplementação do LIBSVM e uma versão do Pegasos), máquinas de vetores de relevância (RVM), redes RBF, regressão online, detecção de anomalias, agrupamento (*k-means* com *kernel*) e ordenação de atributos. Os algoritmos aceitam qualquer tipo de dado, desde que exista um *kernel* adequado.
5. **Licença e uso:** licença Boost, que permite uso em projetos abertos e comerciais; não depende de outras bibliotecas e roda em Windows, Linux e macOS.

## Limitações

- É uma descrição de software, sem experimentos nem comparações de desempenho.
- A versão de 2009 não tem redes neurais profundas; elas foram acrescentadas à dlib depois.

## Ligação com o TCC

- **No benchmark, o modelo Dlib ficou em terceiro lugar:** 84,64% com o detector do OpenCV e 84,90% com o RetinaFace. Quase não mudou com o detector, ao contrário do ArcFace e do VGG-Face, que ganharam bastante com o RetinaFace. Ocupa cerca de 22 MB, bem menos que o ArcFace (130 MB) e o VGG-Face (580 MB).
- Teve precisão alta e *recall* baixo (70,8% e 71,9%), o mesmo padrão do SFace e do GhostFaceNet, que a Visão Geral atribui ao limiar padrão conservador.
- A dlib também aparece no OpenFace: é dela o detector de 68 pontos do rosto usado no alinhamento.
- Na monografia, ao citar o Dlib, explique que o artigo é da biblioteca e que o modelo de reconhecimento facial é documentado no site do projeto.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Por que este artigo não basta para descrever o modelo Dlib usado no benchmark?
2. Que tipo de algoritmo a Dlib-ml de 2009 oferecia?
3. Em que outro trabalho da pasta a dlib aparece, e com qual função?
