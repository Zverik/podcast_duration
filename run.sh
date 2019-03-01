#!/bin/bash
set -e -u
./get_podcast_lengths.py
./parse_vk.py https://vk.com/podcasts-54456105 ~/Downloads/linkmeup.html
./by_hand.py https://itunes.apple.com/podcast/id384460470?mt=2 35,50,39,43,45,62,49,40,65,87,45,67,40,39,36,49,42,26,43,41
./by_hand.py /id1209769632?mt=2 37,35,41,32,28,29,25,26,26,27
./by_hand.py https://itunes.apple.com/ru/podcast/podkast-razbor-poletov/id594292319?mt=2 42,83,56,112,120,47,147,42,41,54,61,48,40,41,38,120,50,38,40,20,130
./by_hand.py https://itunes.apple.com/ru/podcast/drupal-podkasty/id1088466298?mt=2 94,93,61,67,44,41,82,57,104,35,27,37,44,58,56,53,55,43,37,80,62,26,51,40
./by_hand.py /id877524123?mt=2 74,36,24,29,37,29,37,24,32,41,41,31,48,28,43,39,35
./by_hand.py /id263217309?mt=2 18,33,19,23,24
./calculate_minutes.py
