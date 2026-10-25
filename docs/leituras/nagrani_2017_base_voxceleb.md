# Guia de leitura: base VoxCeleb para identificação de locutor (Nagrani *et al.*, 2017)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais da ISCA, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** NAGRANI, A.; CHUNG, J. S.; ZISSERMAN, A. VoxCeleb: a large-scale speaker identification dataset. In: *Interspeech 2017*, Stockholm, p. 2616–2620, 2017. DOI 10.21437/Interspeech.2017-950.
> **PDF local:** `docs/Referencias/nagrani_2017_base_voxceleb.pdf` · **Chave no .bib:** `nagrani2017voxceleb`

---

## Em uma frase

O artigo cria a VoxCeleb, uma base grande de falas de celebridades tiradas de vídeos do YouTube, montada de forma automática com visão computacional. Também mostra que uma rede convolucional supera os métodos clássicos de reconhecimento de locutor nessa base.

## Por que a base foi criada

As bases de locutor existentes eram pequenas, anotadas à mão ou gravadas em condições controladas (telefone, laboratório, gravação limpa). A mais próxima de condições reais, a SITW, tinha 299 locutores anotados manualmente. Os autores querem uma base grande, com o ruído do mundo real, sem depender de anotação manual. É o mesmo raciocínio que levou à LFW para rostos.

## Números da base

- Mais de 100 mil falas de **1.251 celebridades** (a Tabela 1 do artigo indica cerca de 145 mil).
- Equilibrada por gênero (55% de homens), com várias etnias, sotaques, profissões e idades.
- Por pessoa: de 8 a 36 vídeos (média de 18) e de 45 a 250 falas (média de 116). Cada fala dura de 4 s a 145 s, com média de 8,2 s.
- Ambientes variados: tapete vermelho, estádio ao ar livre, entrevistas em estúdio, discursos para plateias, vídeos gravados com celular. Todos têm ruído real: conversa de fundo, risadas, fala sobreposta, acústica da sala e equipamentos de gravação de qualidade variada.

## Como a base foi montada (sem anotação manual)

1. **Lista de pessoas:** parte das 2.622 identidades da base de rostos VGG Face.
2. **Vídeos:** baixa os 50 primeiros vídeos do YouTube para cada nome, com "interview" na busca.
3. **Rastreamento de rostos:** detecta e acompanha os rostos em cada quadro do vídeo.
4. **Quem está falando:** a rede SyncNet verifica se o movimento da boca está sincronizado com o áudio, para achar o rosto que fala.
5. **Quem é a pessoa:** uma rede de reconhecimento facial (VGG Face) confirma se o rosto que fala é a celebridade procurada.

Os limiares das etapas 4 e 5 foram escolhidos de forma conservadora, com precisão de 100% nos testes de referência, para evitar falas atribuídas à pessoa errada. O custo é perder parte das falas válidas.

## Experimentos

- **Identificação** (dizer quem fala entre as 1.251 pessoas): a rede convolucional, adaptada da VGG-M para espectrogramas, acertou **80,5%** na primeira opção (top-1), contra 60,8% do melhor método clássico (i-vectors + PLDA + SVM).
- **Verificação** (dizer se duas falas são da mesma pessoa): as pessoas com nome começando por "E" ficam só para teste. A EER foi de **7,8%** com a rede treinada para gerar *embeddings*, contra 8,8% do i-vector + PLDA e 15,0% do GMM-UBM.
- Para verificação, os autores observam que treinar a rede para gerar um *embedding* (rede siamesa com perda contrastiva) funciona melhor do que reaproveitar uma camada do classificador.

## Limitações

- São celebridades adultas falando em entrevistas e eventos: não há crianças, e o tipo de ruído é diferente do de um veículo.
- A base depende da lista de nomes e dos limiares conservadores, então algumas falas válidas ficam de fora.
- Os resultados de 2017 já foram superados por modelos mais novos: o ECAPA-TDNN chega a EER de 1,01% no VoxCeleb1, contra 7,8% aqui.

## Ligação com o TCC

- É para a voz o que a **LFW** é para o rosto: base pública, de adultos, em condições não controladas. Atende à restrição do projeto de não usar dados de alunos na prototipagem (RC-01).
- É a base em que o ECAPA-TDNN foi treinado (VoxCeleb2) e testado (VoxCeleb1). Um benchmark de voz no TCC2 usaria o mesmo protocolo, o que permite comparar os números com a literatura.
- A diferença entre identificação e verificação é a mesma do rosto. O dispositivo do projeto faz identificação entre cerca de 20 alunos, enquanto o benchmark mede verificação 1:1. É a mesma limitação já registrada para o benchmark facial.
- O próprio processo de montagem da base usa reconhecimento facial e detecção de quem está falando. É um exemplo de rosto e voz usados juntos, embora com outro objetivo.
- Citado na Visão Geral, no parágrafo de reconhecimento de voz (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Qual a diferença entre identificação e verificação de locutor, e qual das duas o dispositivo do projeto faz?
2. Como os autores garantem que a voz de um vídeo é mesmo da celebridade, sem ouvir as gravações?
3. Por que a VoxCeleb é útil para o TCC mesmo sem ter crianças nem ruído de ônibus?
4. O que mudou entre a EER de 7,8% deste artigo e a de 1,01% do ECAPA-TDNN?
