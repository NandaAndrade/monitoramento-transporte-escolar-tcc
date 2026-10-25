# Guia de leitura: ECAPA-TDNN, verificação de locutor (Desplanques *et al.*, 2020)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais da ISCA, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** DESPLANQUES, B.; THIENPONDT, J.; DEMUYNCK, K. ECAPA-TDNN: Emphasized Channel Attention, Propagation and Aggregation in TDNN Based Speaker Verification. In: *Interspeech 2020*, Shanghai, p. 3830–3834, 2020. DOI 10.21437/Interspeech.2020-2650.
> **PDF local:** `docs/Referencias/desplanques_2020_ecapa_tdnn_verificacao_locutor.pdf` · **Chave no .bib:** `desplanques2020ecapa`

---

## Em uma frase

O ECAPA-TDNN é uma rede que transforma um trecho de fala de qualquer duração num vetor de tamanho fixo (*embedding*) que identifica quem está falando. Ela melhora a arquitetura x-vector com atenção por canal, blocos residuais e agregação de várias camadas.

## O problema

A verificação de locutor responde à pergunta "esta fala é da pessoa X?". O padrão da época era o **x-vector**: uma rede de atraso temporal (TDNN, uma sequência de convoluções 1D sobre o tempo) seguida de uma camada que resume a fala inteira pela média e pelo desvio-padrão das ativações. Os autores apontam três limitações:

- cada camada só enxerga um contexto curto, de cerca de 15 quadros;
- o resumo trata todos os quadros e todos os canais da mesma forma, embora alguns trechos da fala digam mais sobre o locutor do que outros;
- só a última camada entra no *embedding*, e as camadas intermediárias também guardam informação útil.

## A ideia central

1. **Pooling com atenção por canal e contexto global.** Em vez da média simples, a rede aprende um peso para cada quadro, separadamente em cada canal, e calcula uma média e um desvio-padrão ponderados. A atenção também recebe a média e o desvio-padrão da fala inteira, para decidir o peso de cada quadro olhando o todo.
2. **Blocos SE-Res2Block.** São blocos residuais que combinam duas ideias da visão computacional: o *Squeeze-Excitation*, que dá a cada canal um peso calculado a partir da fala inteira, e o *Res2Net*, que processa várias escalas de tempo dentro do mesmo bloco.
3. **Agregação de várias camadas.** As saídas de todos os blocos são concatenadas antes do pooling, e não só a do último.
4. **Treino com margem angular.** A perda usada é a AAM-softmax, com margem de 0,2: é a mesma ideia do **ArcFace**, que o artigo cita como referência. Para ver se duas falas são da mesma pessoa, compara-se a **distância de cosseno** entre os *embeddings*.

## Como foi treinado e testado

- **Treino:** parte de desenvolvimento do VoxCeleb2, com 5.994 locutores. Cada fala recebeu 6 versões extras com aumento de dados: ruído e fala de fundo (base MUSAN), reverberação, mudança de velocidade e compressão de áudio. Também foi aplicado o SpecAugment, que apaga pedaços aleatórios do espectrograma.
- **Entrada:** 80 coeficientes MFCC, com janela de 25 ms e passo de 10 ms, em recortes de 2 s.
- **Teste:** conjuntos do VoxCeleb1 (o original e as listas mais difíceis, VoxCeleb1-E e VoxCeleb1-H) e a avaliação do desafio VoxSRC 2019. As métricas são a **EER** (taxa de erro igual, o ponto em que falsos aceites e falsas rejeições se igualam) e a MinDCF.

## Resultados principais

- **Versão menor (C = 512):** 6,2 milhões de parâmetros e EER de 1,01% no VoxCeleb1.
- **Versão maior (C = 1024):** 14,7 milhões de parâmetros e EER de 0,87% no VoxCeleb1.
- As duas superaram todas as referências (x-vector estendido e r-vector com ResNet), mesmo com menos parâmetros. A versão maior teve melhora relativa média de 18,7% na EER sobre a melhor referência em cada conjunto de teste.
- **Ablação:** os blocos SE foram o componente que mais pesou; sem eles, a EER da versão menor sobe de 1,01% para 1,27%.

## Limitações

- Todos os testes são com celebridades adultas em vídeos da internet (VoxCeleb). Não há teste com crianças nem com o ruído de um veículo.
- O ruído entra só como aumento de dados no treino. O artigo não mede o desempenho em função do nível de ruído.
- Não há medição de tempo de inferência nem teste em hardware embarcado. Os 6,2 milhões de parâmetros são poucos para um servidor, mas o artigo não diz se o modelo roda bem num Raspberry Pi.

## Ligação com o TCC

- Mostra que a voz pode seguir **o mesmo esquema do rosto**: extrair um *embedding*, comparar pela distância de cosseno com o cadastrado e decidir por um limiar. A perda é até parente do ArcFace. Isso permitiria reaproveitar no software embarcado a mesma lógica de comparação com a galeria de referências.
- É o candidato natural de referência para o benchmark de voz do TCC2, como o ArcFace foi para o rosto.
- O tamanho (6,2 milhões de parâmetros na versão menor) é um bom ponto de partida para a análise de hardware, mas a viabilidade no Raspberry Pi precisa vir de outra fonte (por exemplo, Chen *et al.*, 2023, que ainda não está na pasta) ou de medição própria.
- O treino com ruído e reverberação é um bom sinal, mas o ruído do ônibus (motor, estrada, conversa dos alunos) é diferente do ruído dos vídeos do VoxCeleb. Vale testar com gravações ou ruído simulado do ônibus.
- Citado na Visão Geral, no parágrafo de reconhecimento de voz (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. O que a camada de pooling faz com uma fala de duração variável, e o que a atenção por canal muda nesse cálculo?
2. Qual a semelhança entre a perda AAM-softmax usada aqui e o ArcFace?
3. O que significa uma EER de 1,01%?
4. Por que os resultados no VoxCeleb não garantem o desempenho dentro do ônibus?
