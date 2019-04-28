#Zctp

Zctp is a tool for word frequency analysis in clinical area. Because clinical texts are different from other texts, many text processing tools, such as jieba, can not finish tasks satisfactorily. Hence I proposed an algorithm based on jieba, inspired from k-mer counting algorithms, to help our team finish clinical data analysis.

Sketch of algorithm:
--------
I only explain how the function named cat works, for the function named dog is too simple.

```
D: the array where texts of diagnosis are stored
W: the array where words are stored
N: the max amount of words to be combined
T: the threshold of frequency, words whose frequency < T will not be added to W
```
```
D = jieba.lcut(D)
for i in [N:1]:
    for j in [0:length(D)-1]:
        for k in [0:length(D[j])-1]:
            W[i].words.append(D[j][k:k+N])
            W[i].frequency.append(1)
    W[i] = groupby(W[i].words)
    W[i] = W[i].sum(frequency)
    W[i] = filter(W[i].frequency, T)
    if i<N:
        for j in [0:length(W[i])-1]:
            if W[i][j] is not matched in W[i+1]:
                W[i] = W[i+1].append(W[i][j])
return w[1]
```

Result:
--------
```
Sample:
N = 3    T = 2
D = 
反复发作性发热
结核性肺炎
颅内感染，呼吸衰竭
肺炎；肺部感染
肺大泡，矽肺病，持续发热10天，T：38.5度，尿检异常，大便里霉菌
恶性肿瘤，癌灶发热
肺结核，左侧包裹性脓胸（伤口3月不愈合。怀疑其它细菌，真菌感染）
腿部残疾，肺部感染
多发伤；神智不清
中枢神经系统感染
肺部感染，II型呼吸衰竭
中枢神经系统感染
发热原因待查：感染性？免疫性？
双肺粟粒影（血播可能），结核性脑膜炎
中枢神经系统感染
重型颅脑损伤，肺部感染
```
```
jieba:
            16
，            13
感染            9
发热            4
肺部            4
中枢神经          3
系统            3
性             2
呼吸衰竭          2
；             2
：             2
（             2
）             2
？             2
```
```
Zctp:
肺部感染	4
发热	4
中枢神经系统感染	3
呼吸衰竭  2
```
