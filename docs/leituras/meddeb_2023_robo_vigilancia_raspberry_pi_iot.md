# Guia de leitura: robô de vigilância com reconhecimento facial em Raspberry Pi e IoT (Meddeb *et al.*, 2023)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (Elsevier), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** MEDDEB, H.; ABDELLAOUI, Z.; *et al.* Development of surveillance robot based on face recognition using Raspberry-PI and IOT. *Microprocessors and Microsystems*, v. 96, artigo 104728, 2023. Confira a lista completa de autores e o DOI na página do artigo.
> **PDF local:** `Downloads/Referencias/meddeb_2023_robo_vigilancia_raspberry_pi_iot.pdf`

---

## Em uma frase

Os autores constroem um robô móvel de baixo custo, com Raspberry Pi 4, câmera e sensor de presença, que patrulha áreas industriais, reconhece rostos e avisa uma sala de controle via IoT quando encontra um intruso.

## O sistema

1. **Hardware:** Raspberry Pi 4, câmera, sensor infravermelho passivo (PIR) para detectar movimento, motores para deslocar o robô.
2. **Fluxo:** o PIR detecta alguém; a câmera captura vídeo e fotos; o rosto é detectado e comparado com os cadastrados; se for desconhecido, o sistema manda alerta, foto e vídeo para a sala de controle pela Internet.
3. **Reconhecimento:** usa o método LBPH (padrões binários locais, o mesmo de Ahonen *et al.*, 2004), escolhido por ser leve.
4. **Avaliação:** testes com uma base pequena (15 pessoas), variando o número de pessoas cadastradas (5, 10, 15 e 20) e medindo taxa de identificação, taxa de falsos negativos e acurácia.

## Resultados

- O LBPH funcionou em tempo real no Raspberry Pi 4, com taxas de acerto altas na base pequena; os valores exatos estão na Tabela 2 e na Figura 16 do PDF.
- **Cuidado:** a Tabela 3 do artigo, que compara Eigenface (77,9%), Fisherface (85,2%), SVM (90,6%) e CNN (93,3%), traz números de **outro trabalho**, citado pelos autores, e não de experimentos deles. O [documento de lacunas](../lacunas_revisao_bibliografica.md) (item E3) já registra que os 93% atribuídos a esse artigo vêm de bases pequenas e controladas.

## Limitações

- Base própria muito pequena, em condições controladas.
- Envia imagens das pessoas pela rede, o que no caso do projeto seria inaceitável pela LGPD.
- LBPH é sensível a pose e sombras.

## Ligação com o TCC

- Exemplo de arquitetura **IoT com Raspberry Pi + sensor + câmera + aviso remoto**, muito próxima da do projeto, útil para a revisão bibliográfica e para a Atividade 1.3.
- O uso de um sensor PIR para "acordar" o sistema é uma ideia aproveitável para economizar energia no ônibus: só processar quando alguém se aproxima da porta.
- **Contraste importante:** o robô transmite fotos e vídeos; o projeto, por causa da LGPD, não deixa nenhuma imagem sair do dispositivo (RF-05).

## Perguntas para conferir a leitura

1. Quais números da avaliação são dos próprios autores e quais vêm de outros trabalhos?
2. Por que o LBPH foi escolhido em vez de uma rede profunda?
3. Que parte da arquitetura do robô o projeto poderia aproveitar, e que parte violaria a LGPD?
