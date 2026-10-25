# Guia de leitura: detecção de rostos com cascata de classificadores, o "Haar Cascade" (Viola e Jones, 2001)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** VIOLA, P.; JONES, M. Rapid Object Detection using a Boosted Cascade of Simple Features. In: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2001. Páginas a conferir (o PDF é a versão aceita, sem paginação).
> **PDF local:** `docs/Referencias/viola_2001_haar_cascade.pdf` · **Chave no .bib:** `viola2001haar`

---

## Em uma frase

O artigo apresenta um detector de rostos de frente extremamente rápido, baseado em características simples do tipo Haar, calculadas com a "imagem integral", escolhidas pelo AdaBoost e organizadas numa cascata que descarta rapidamente as regiões sem rosto. É o detector "Haar Cascade" do OpenCV.

## As três contribuições

1. **Imagem integral.** Uma tabela pré-calculada em que cada posição guarda a soma de todos os pixels acima e à esquerda. Com ela, a soma de qualquer retângulo da imagem sai com poucas operações, em tempo constante. Isso torna baratas as características do tipo Haar, que são diferenças entre somas de retângulos claros e escuros (por exemplo, a região dos olhos é mais escura que a das bochechas).
2. **Seleção de características com AdaBoost.** Há muito mais características possíveis do que dá para calcular. O AdaBoost escolhe poucas, as mais úteis, e combina classificadores simples num classificador forte. Um classificador com só duas características já detecta todos os rostos de validação, com 40% de falsos positivos.
3. **Cascata.** Os classificadores ficam em sequência, do mais simples ao mais complexo. Cada janela da imagem passa pelo primeiro; se ele disser "não é rosto", a janela é descartada na hora. Só as janelas promissoras chegam aos estágios mais caros. Como a maior parte da imagem não tem rosto, quase tudo é descartado nos primeiros estágios.

## Treino

- 4.916 rostos rotulados à mão, reduzidos a 24 × 24 pixels (9.832 com os espelhados), e 9.544 imagens sem rosto.
- A cascata final tem **38 estágios e mais de 6.000 características**. Em média, só cerca de 10 características são avaliadas por janela.

## Resultados principais

- Taxas de detecção e de falsos positivos equivalentes às dos melhores detectores da época, na base de teste MIT+CMU (130 imagens, 507 rostos).
- **Velocidade:** cerca de 0,067 s por imagem de 384 × 288 pixels num Pentium III de 700 MHz, ou seja, uns **15 quadros por segundo**. Cerca de 15 vezes mais rápido que o detector de Rowley, Baluja e Kanade, e 600 vezes mais que o de Schneiderman e Kanade.

## Limitações (do artigo ou evidentes hoje)

- O artigo treina o detector só para **rostos de frente e na vertical**. Rostos de lado, inclinados ou parcialmente cobertos ficam fora do que ele foi feito para detectar.
- As características medem contraste de luz entre regiões do rosto, então iluminação forte ou irregular tende a atrapalhar. O artigo não testa isso.
- Os detectores com redes profundas (RetinaFace, YuNet) superaram este método em precisão, principalmente com rostos pequenos e em condições difíceis.

## Ligação com o TCC

- **É o detector "OpenCV" do benchmark.** Foi o detector rápido da primeira rodada: cerca de 0,02 s por imagem, contra cerca de 0,6 s do RetinaFace na mesma CPU. Mas a acurácia dos modelos caiu com ele (o ArcFace foi de 96,61% com o RetinaFace para 92,97% com o OpenCV).
- A limitação a rostos de frente pesa na porta do ônibus, onde o aluno passa em movimento e nem sempre olha para a câmera. Isso reforça a busca por um detector moderno e leve, como o YuNet, que é o próximo passo do benchmark.
- A ideia da cascata (descartar cedo o que é fácil e gastar processamento só no que importa) é útil no dispositivo: por exemplo, só rodar o reconhecimento quando um rosto for detectado.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Para que serve a imagem integral?
2. Por que a cascata deixa o detector tão rápido?
3. Que limitação do Haar Cascade pesa mais no cenário do ônibus?
4. Qual foi a troca entre tempo e acurácia ao usar este detector no benchmark do TCC?
