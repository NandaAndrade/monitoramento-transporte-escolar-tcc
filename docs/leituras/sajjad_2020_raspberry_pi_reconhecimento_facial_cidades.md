# Guia de leitura: reconhecimento facial com Raspberry Pi e nuvem para segurança pública (Sajjad *et al.*, 2020)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (Elsevier), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** SAJJAD, M.; NASIR, M.; MUHAMMAD, K.; KHAN, S.; JAN, Z.; SANGAIAH, A. K.; ELHOSENY, M.; BAIK, S. W. Raspberry Pi assisted face recognition framework for enhanced law-enforcement services in smart cities. *Future Generation Computer Systems*, v. 108, p. 995–1007, 2020. DOI: [10.1016/j.future.2017.11.013](https://doi.org/10.1016/j.future.2017.11.013).
> **PDF local:** `Downloads/Referencias/sajjad_2020_raspberry_pi_reconhecimento_facial_cidades.pdf`
>
> **Atenção:** a extração de texto deste PDF perdeu os espaços entre palavras, então alguns detalhes não puderam ser conferidos com precisão. Confira os números das tabelas no original.

---

## Em uma frase

Os autores propõem uma câmera escondida no uniforme de um policial, ligada a um Raspberry Pi que detecta rostos no vídeo, enquanto o **classificador é treinado e guardado na nuvem**, por causa da memória e do processamento limitados do Raspberry Pi.

## O sistema

1. **Captura:** uma câmera sem fio pequena, presa ao uniforme, envia o vídeo ao Raspberry Pi 3 Modelo B.
2. **Detecção:** feita no próprio Raspberry Pi.
3. **Descrição do rosto:** pontos-chave ORB (*oriented FAST and rotated BRIEF*), agrupados em um "saco de palavras visuais" (*bag of words*), o que gera um vetor de tamanho fixo para cada rosto.
4. **Classificação:** uma máquina de vetores de suporte (SVM) identifica se o rosto é de um suspeito cadastrado.
5. **Divisão borda-nuvem:** o treino e o armazenamento do classificador ficam na nuvem; o Raspberry Pi faz a captura e a detecção.
6. Implementação em Python 2.7 com OpenCV no Raspberry Pi 3.

## Resultados

- Testes em várias bases públicas de rostos, com variação do número de imagens de treino, do tamanho do vocabulário visual e da validação cruzada. Em uma das bases (face-95), a acurácia média variou de cerca de 89% a 100% conforme a configuração.
- Os próprios autores observam que nenhum método é o melhor em todas as situações: o resultado muda com textura, tamanho, intensidade de cor e escala das imagens.

## Limitações

- Usa características clássicas (ORB + saco de palavras + SVM), não redes profundas.
- Depende de conexão com a nuvem para a identificação.
- Uso por forças policiais levanta questões éticas e de privacidade que o artigo pouco discute.

## Ligação com o TCC

- É o contraponto direto da decisão do projeto de fazer o reconhecimento **inteiro no dispositivo**: aqui, parte do processamento vai para a nuvem por falta de recursos (item A1 do [documento de lacunas](../lacunas_revisao_bibliografica.md)). Nas rotas rurais, com internet instável, essa divisão não funcionaria; e com o Hailo, já não é necessária.
- Bom exemplo de "por que não": serve para justificar a computação de borda na revisão bibliográfica.

## Perguntas para conferir a leitura

1. O que fica no Raspberry Pi e o que fica na nuvem, e por quê?
2. O que acontece com esse sistema se a conexão cair, e como o projeto resolve o mesmo problema?
3. Como o "saco de palavras visuais" transforma um número variável de pontos-chave em um vetor de tamanho fixo?
