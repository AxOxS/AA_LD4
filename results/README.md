# Algoritmo analizės projekto pristatymas

## 1. Projekto struktūra ir organizacija

Projektas organizuotas pagal šiuolaikines programinės įrangos kūrimo praktikas, su aiškia moduline struktūra:

```
algorithm-analysis/
├── src/                     # Šaltinio kodas
│   ├── algorithms/          # Algoritmų implementacijos
│   │   ├── subset_sum.py    # Poaibio sumos algoritmai 
│   │   └── shortest_path.py # Trumpiausio kelio algoritmas
│   ├── benchmarks/          # Testavimo scenarijai
│   │   ├── subset_sum_benchmark.py
│   │   ├── shortest_path_benchmark.py
│   │   └── compare_algorithms.py
│   └── utils/               # Pagalbinės funkcijos
│       ├── graph_utils.py   # Grafų generavimas
│       ├── plotting.py      # Rezultatų vizualizacija
│       └── timer.py         # Laiko matavimo įrankiai
├── tests/                   # Testavimo skriptai
│   ├── test_subset_sum.py   # Poaibio sumos testai
│   ├── test_shortest_path.py # Trumpiausio kelio testai
│   └── test_utils.py        # Įrankių testai
├── results/                 # Rezultatų katalogas
├── main.py                  # Pagrindinis vykdomasis failas
└── requirements.txt         # Priklausomybės
```

## 2. Teorinis sudėtingumo įvertinimas

### Poaibio sumos uždavinys (NP-pilna klasė)

Poaibio sumos uždavinys: turint aibę skaičių, rasti tokį poaibį, kurio suma lygi nurodytam tikslui.

Implementuoti trys algoritmai:

1. **Backtracking algoritmas:**
```python
def subset_sum_backtracking(nums: List[int], target: int) -> bool:
    def backtrack(index: int, current_sum: int) -> bool:
        # Bazinis atvejis
        if current_sum == target:
            return True
        
        if index >= len(nums) or current_sum > target:
            return False
        
        # Įtraukti elementą
        if backtrack(index + 1, current_sum + nums[index]):
            return True
        
        # Neįtraukti elemento
        if backtrack(index + 1, current_sum):
            return True
        
        return False
    
    # Optimizacija
    nums = [n for n in nums if n <= target]
    nums.sort()
    
    return backtrack(0, 0)
```

**Teorinis sudėtingumas:** O(2^n) - eksponentinis, kur n yra skaičių kiekis.

2. **Dinaminio programavimo algoritmas:**
```python
def subset_sum_dynamic(nums: List[int], target: int) -> bool:
    # Filtruojame skaičius, didesnius už tikslą
    nums = [n for n in nums if n <= target]
    
    # Sukuriame DP lentelę
    dp = [False] * (target + 1)
    dp[0] = True  # Tuščio poaibio suma lygi 0
    
    for num in nums:
        for i in range(target, num - 1, -1):
            dp[i] = dp[i] or dp[i - num]
    
    return dp[target]
```

**Teorinis sudėtingumas:** O(n * target) - pseudo-polinominis, priklauso nuo skaičių kiekio ir tikslinio skaičiaus dydžio.

3. **Išsamios paieškos algoritmas (blogiausiam atvejui):**
```python
def subset_sum_exhaustive(nums: List[int], target: int) -> bool:
    def backtrack(index, current_sum):
        if index == len(nums):
            return current_sum == target
        
        # Visada tiria abi šakas
        include = backtrack(index + 1, current_sum + nums[index])
        exclude = backtrack(index + 1, current_sum)
        
        return include or exclude
    
    return backtrack(0, 0)
```

**Teorinis sudėtingumas:** O(2^n) - eksponentinis, garantuotai visada patikrina visas galimas kombinacijas.

### Trumpiausio kelio uždavinys (P klasė)

Trumpiausio kelio uždavinys: turint svorinį grafą, rasti trumpiausią kelią nuo pradinio viršūnės iki visų kitų viršūnių.

**Dijkstra algoritmas:**
```python
def dijkstra_shortest_path(graph: Graph, start: Vertex) -> Dict[Vertex, Weight]:
    # Inicializuojame atstumus
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    
    # Prioritetinė eilė
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Jei jau radome trumpesnį kelią, praleidžiame
        if current_distance > distances[current_vertex]:
            continue
        
        # Tikriname visus kaimynus
        for neighbor, weight in graph[current_vertex]:
            distance = current_distance + weight
            
            # Jei radome trumpesnį kelią, atnaujiname
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances
```

**Teorinis sudėtingumas:** O(E + V log V), kur E yra briaunų skaičius, o V - viršūnių skaičius. Tankiame grafe tai apytiksliai O(n²).

## 3. Eksperimentinis tyrimas

### Techninė įranga
- CPU: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel
- RAM: 31.43GB
- OS: Windows 11

### Poaibio sumos algoritmo rezultatai

#### Backtracking algoritmas
Testai atlikti su įvesties dydžiais: 5, 10, 15, 20, 22, 24, 26, 28, 30

```
Testing size 5...  → Average: 6.60 μs
Testing size 10... → Average: 19.07 μs
Testing size 15... → Average: 28.93 μs
Testing size 20... → Average: 35.13 μs
Testing size 22... → Average: 130.02 ms
Testing size 24... → Average: 379.32 μs
Testing size 26... → Average: 1.37 ms
Testing size 28... → Average: 138.31 ms
Testing size 30... → Average: 551.41 ms
```

#### Dinaminis programavimas
Testai atlikti su įvesties dydžiais: 5, 10, 20, 50, 100, 200, 500, 1000

```
Testing size 5...   → Average: 26.86 μs
Testing size 10...  → Average: 76.13 μs
Testing size 20...  → Average: 382.03 μs
Testing size 50...  → Average: 1.93 ms
Testing size 100... → Average: 8.85 ms
Testing size 200... → Average: 26.88 ms
Testing size 500... → Average: 198.87 ms
Testing size 1000...→ Average: 715.44 ms
```

#### Blogiausio atvejo testavimas (išsamus)
Testai atlikti su įvesties dydžiais: 10, 12, 15, 18, 20, 22, 25

```
Testing size 10... → Time: 173.57 μs
Testing size 12... → Time: 391.24 μs
Testing size 15... → Time: 2.93 ms
Testing size 18... → Time: 23.61 ms
Testing size 20... → Time: 95.14 ms
Testing size 22... → Time: 390.54 ms
Testing size 25... → Time: 3.2580 s
```

### Trumpiausio kelio algoritmo rezultatai

Testai atlikti su įvesties dydžiais: 10, 50, 100, 200, 500, 1000, 1500, 2000

```
Testing size 10...   → Average: 7.63 μs
Testing size 50...   → Average: 99.26 μs
Testing size 100...  → Average: 235.95 μs
Testing size 200...  → Average: 709.45 μs
Testing size 500...  → Average: 4.25 ms
Testing size 1000... → Average: 18.51 ms
Testing size 1500... → Average: 34.38 ms
Testing size 2000... → Average: 58.12 ms
```

## 4. Rezultatų analizė ir palyginimas

### Eksperimentiškai nustatytos augimo funkcijos

Iš algoritmo analizės ataskaitos (`algorithm_analysis_report.txt`):

```
NP-COMPLETE ALGORITHM (SUBSET SUM - BACKTRACKING):
Tested sizes: [5, 10, 15, 20, 22, 24, 26, 28]
Execution times (s): [9e-06, 4.9e-05, 0.000163, 0.00045, 0.138637, 5.2e-05, 4.513633, 17.874904]
Experimentally determined growth rate: n^6.766979757846671
Theoretical complexity: O(2^n)

POLYNOMIAL ALGORITHM (DIJKSTRA'S SHORTEST PATH):
Tested sizes: [10, 50, 100, 200, 500, 1000]
Execution times (s): [1e-05, 8.9e-05, 0.000236, 0.000837, 0.004286, 0.01622]
Experimentally determined growth rate: n^1.6057419286308237
Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs
```

### Pastabos dėl eksperimentinių augimo funkcijų

1. **Poaibio suma (backtracking)**: Eksperimentiškai nustatyta augimo funkcija n^6.77 neatspindi tikrosios eksponentinės funkcijos O(2^n) dėl kelių priežasčių:
   - Su mažesniais įvesties dydžiais eksponentinis augimas dar nėra toks ryškus
   - Algoritmo optimizacijos (rikiavimas ir filtravimas) pagerina darbą kai kuriems atvejams
   - Matome nereguliarų vykdymo laiką (pvz., mažesnis laikas prie n=24 nei prie n=22), nes atsitiktinai generuojami testiniai atvejai gali būti "lengvi" arba "sunkūs" algoritmui
   - Analizuojant 26, 28 ir 30 dydžio įvestis, kai kuriais atvejais matome labai ilgą vykdymo laiką (iki 26.9s), kas aiškiau rodo eksponentinį augimą

2. **Poaibio suma (blogiausias atvejis)**: Specialiai sukonstruoti blogiausio atvejo scenarijai aiškiau parodo eksponentinį augimą. Pavyzdžiui, vykdymo laikas auga nuo 390.54 ms su n=22 iki 3.26s su n=25, tai yra, pridėjus tik 3 papildomus elementus, vykdymo laikas išauga daugiau nei 8 kartus.

3. **Trumpiausias kelias**: Eksperimentiškai nustatyta augimo funkcija n^1.61 gerai atitinka teorinį O(n²) sudėtingumą tankiems grafams. Matome nuoseklų augimą nuo 7.63 μs (n=10) iki 58.12 ms (n=2000).

### Grafinė vizualizacija

Projektas sugeneravo keletą grafikų, parodančių algoritmų vykdymo laiką:

1. **algorithm_comparison.png** - Tiesioginis P ir NP-pilnos klasės algoritmų palyginimas
2. **subset_sum_backtracking.png** - Poaibio sumos backtracking algoritmo veikimas
3. **subset_sum_dp.png** - Poaibio sumos dinaminio programavimo algoritmo veikimas
4. **subset_sum_worst_case.png** - Poaibio sumos blogiausio atvejo analizė
5. **shortest_path.png** - Trumpiausio kelio algoritmo veikimas

Grafikai naudoja logaritminę skalę y ašiai, kad būtų galima aiškiau pamatyti eksponentinį ir polinominį augimą.

## 5. Įdomūs pastebėjimai

1. **Dinaminis programavimas vs. Backtracking**:
   - Dinaminis programavimas gali apdoroti daug didesnius įvesties dydžius (iki n=1000)
   - Backtracking algoritmas yra ženkliai greitesnis mažoms įvestims, bet labai greitai tampa neefektyvus
   - Blogiausio atvejo scenarijai rodo tikrąjį eksponentinį augimą, kai visi poaibiai turi būti ištirti

2. **Eksperimentinės ir teorinės sudėtingumo funkcijos**:
   - Eksperimentinės funkcijos ne visada tiksliai atitinka teorines dėl įvairių faktorių
   - Tiek optimizacijos, tiek konkretūs testiniai atvejai gali stipriai paveikti faktinį vykdymo laiką

3. **Įdomūs stebėjimai vykdymo laikuose**:
   - Tam tikros įvesties reikšmės (n=22, n=26, n=28) rodo labai nereguliarų vykdymo laiką
   - Kai kurie testai baigiasi anksčiau dėl ankstyvojo nutraukimo strategijų backtracking algoritme
   - Didėjant duomenų dydžiui, skirtumas tarp P ir NP-pilnos klasės algoritmų tampa vis akivaizdesnis

## 6. Stebėti netikslumai ir variabilumas

Analizuojant rezultatus pastebėta keletas reikšmingų netikslumų ir variabilumų, kurie verti atskiros diskusijos:

1. **Backtracking algoritmo rezultatų nepastovumas**:
   - Ženklūs vykdymo laiko svyravimai tarp testų su ta pačia n reikšme
   - Kai kuriems atvejams (n=24) laikai netikėtai maži lyginant su mažesnėmis įvestimis (n=22)
   - Skirtingi paleidimai pateikia skirtingus rezultatus toms pačioms įvesties reikšmėms
   
   Šis nepastovumas gali būti paaiškintas:
   - Atsitiktinio duomenų generavimo prigimtimi (kai kurie atsitiktinai generuoti atvejai gali būti "lengvi")
   - Backtracking algoritmo ankstyvojo nutraukimo strategijomis
   - Algoritmą pagreitinanačiomis optimizacijomis (pvz., rikiavimas ir filtravimas)

2. **Specifiniai ekstremalūs atvejai**:
   - n=26 bandyme užfiksuotas 6.7s laikas, lyginant su 1.37ms vidurkiu 
   - n=28 bandyme užfiksuotas 26.9s laikas, lyginant su 138.31ms vidurkiu
   
   Tai rodo, kad pateikti vidurkiai ne visada tinkamai atspindi tikrąjį algoritmo sudėtingumą, ypač kai testai pasibaigia labai anksti sėkmės atveju.

3. **Rekomenduojami tobulinimai**:
   - Naudoti fiksuotus testinius atvejus, o ne atsitiktinius, norint užtikrinti pakartojamumą
   - Atlikti daugiau bandymų kiekvienam įvesties dydžiui
   - Išskirti "random" ir "worst case" scenarijų rezultatus
   - Pridėti laiko ribojimą, kad būtų galima tirti didesnius dydžius nerizikuojant per ilgu vykdymo laiku

## 7. Išvados

Šis projektas aiškiai demonstruoja fundamentalų skirtumą tarp P ir NP-pilnos klasės algoritmų:

1. **P klasės algoritmai (Dijkstra)** rodo nuoseklų, prognozuojamą augimu su didesne įvestimi:
   - Vykdymo laikas auga polinomiškai (n^1.61)
   - Gali efektyviai spręsti didelius uždavinius (n=2000) per priimtiną laiką
   - Rezultatai yra nuoseklūs ir gerai atitinka teorinį sudėtingumą

2. **NP-pilnos klasės algoritmai (Poaibio suma)** demonstruoja problematišką elgseną:
   - Blogiausiu atveju vykdymo laikas auga eksponentiškai
   - Net ir mažos įvestys (n=25) gali užimti reikšmingą laiką (>3s)
   - Egzistuoja dideli vykdymo laiko svyravimai priklausomai nuo konkrečių įvesties duomenų
   - Optimizacijos gali padėti tam tikrais atvejais, tačiau neišsprendžia fundamentalaus eksponentiškumo

3. **Praktinės implikacijos**:
   - NP-pilnos klasės problemoms reikalingi aproksimaciniai algoritmai ar euristikos didelėms įvestims
   - Dinaminis programavimas gali būti naudingas kai kuriais atvejais, bet galiausiai irgi susiduria su ribomis
   - Deterministiniams rezultatams reikėtų naudoti kontroliuojamus testinius rinkinius, ne atsitiktinius

Šie pastebėjimai praktiškai patvirtina teorinę perskyrą tarp P ir NP sudėtingumo klasių ir parodo, kodėl P vs NP klausimas išlieka viena iš svarbiausių neišspręstų problemų kompiuterių moksle.

## 8. Skirtingų kompiuterių palyginimas

Eksperimentai buvo atlikti naudojant du skirtingus kompiuterius:

### Kompiuteris A (pagrindinis):
- CPU: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel
- RAM: 31.43GB
- OS: Windows 11

### Kompiuteris B (antrinis):
- CPU: Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
- RAM: 15.74GB
- OS: Windows 11

### Rezultatų palyginimas

#### NP-Pilna problema (Poaibio suma - Backtracking)

| Kompiuteris | Eksperimentiškai nustatytas augimo greitis | Vykdymo laikas (n=28) |
|-------------|------------------------------------------|---------------------|
| A           | n^6.77                                    | 17.87 s             |
| B           | n^2.62                                   | 0.0016 s            |

#### P problema (Dijkstra trumpiausias kelias)

| Kompiuteris | Eksperimentiškai nustatytas augimo greitis | Vykdymo laikas (n=1000) |
|-------------|------------------------------------------|----------------------|
| A           | n^1.61                                    | 0.0162 s              |
| B           | n^1.54                                   | 0.0263 s             |

### Analizė

1. **Aparatinės įrangos įtaka**:
   - Kompiuteris A turi daugiau RAM (31.43GB vs 15.74GB), tačiau tai neturėjo reikšmingo poveikio algoritmų veikimui, nes testuojami duomenų dydžiai neviršijo RAM apribojimų
   - Skirtingi CPU modeliai (197 vs 140) turi įtakos absoliučiam vykdymo laikui, bet ne augimo funkcijai

2. **Backtracking algoritmo skirtumai**:
   - Kompiuteryje B backtracking algoritmas rodo žymiai mažesnį sudėtingumą (n^2.62 vs n^6.77) ir daug trumpesnį vykdymo laiką (0.0016s vs 17.87s su n=28)
   - Šis dramatiškas skirtumas greičiausiai susijęs su atsitiktinai generuotais testiniais atvejais - kompiuteryje B sugeneruoti "lengvesni" atvejai
   - Tai dar kartą patvirtina, kad atsitiktiniai testiniai atvejai blogai atspindi tikrąjį NP-pilnų problemų sudėtingumą

3. **Dijkstros algoritmo skirtumai**:
   - Abu kompiuteriai rodo panašų teorinį augimo greitį (n^1.61 vs n^1.54), kas atitinka teorinį O(n²) sudėtingumą
   - Kompiuteris A šiek tiek greitesnis (0.0162s vs 0.0263s su n=1000), bet skirtumai nėra tokie dramatiškai dideli

4. **Išvados iš palyginimo**:
   - P klasės algoritmai (Dijkstra) rodo stabilius ir prognozuojamus rezultatus abiejuose kompiuteriuose
   - NP-pilnos klasės algoritmai (Poaibio suma) rodo labai nepastovius rezultatus, priklausomai nuo konkrečių testinių atvejų
   - Tai patvirtina, kad NP-pilnų problemų vykdymo laikas labai priklauso nuo konkrečių įvesties duomenų

Šis palyginimas dar kartą pabrėžia NP-pilnų uždavinių esmę - jų sudėtingumas gali dramatiškai skirtis net ir nedidelėms įvestims, priklausomai nuo konkrečių duomenų, tuo tarpu P klasės algoritmai rodo daug stabilesnį ir prognozuojamesnį elgesį.

## 9. Bibliografija ir šaltiniai

1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). Introduction to Algorithms, 3rd Edition. MIT Press.
2. Knuth, D. E. (1997). The Art of Computer Programming, Volume 1: Fundamental Algorithms, 3rd Edition. Addison-Wesley.
3. Garey, M. R., & Johnson, D. S. (1979). Computers and Intractability: A Guide to the Theory of NP-Completeness. W.H. Freeman.
4. Skiena, S. S. (2020). The Algorithm Design Manual, 3rd Edition. Springer. 
3. Garey, M. R., & Johnson, D. S. (1979). Computers and Intractability: A Guide to the Theory of NP-Completeness. W.H. Freeman.
4. Skiena, S. S. (2020). The Algorithm Design Manual, 3rd Edition. Springer. 

## 10. Rekomendacijos tolimesniam tyrimui

Ateityje planuojant panašius tyrimus, siūlytume įvertinti šiuos aspektus:

1. **Kontroliuojami testiniai duomenys**:
   - Sukurti standartizuotą testinių atvejų rinkinį kiekvienam algoritmo dydžiui
   - Užtikrinti, kad kiekvienas testas turėtų bent kelis "lengvus" ir kelis "sunkius" atvejus
   - Išlaikyti tuos pačius duomenis skirtingoms algoritmų implementacijoms

2. **Išsamesnis NP-pilnų problemų tyrimas**:
   - Ištirti kitas NP-pilnas problemas (pvz., keliaujančio pirklio problema, klikos radimas)
   - Palyginti skirtingų NP-pilnų problemų praktinį sprendžiamumą
   - Ištirti aproksimavimo algoritmus ir jų efektyvumą

3. **Paralelizavimo galimybės**:
   - Ištirti, kaip paralelizavimas gali pagerinti NP-pilnų problemų sprendimą
   - Palyginti skirtingų paralelizavimo strategijų efektyvumą
   - Įvertinti, kaip daug branduolių architektūros gali padėti spręsti sudėtingus uždavinius

4. **Statistinė analizė**:
   - Atlikti daugiau bandymų su kiekvienu įvesties dydžiu (>10 kartų)
   - Pateikti ne tik vidurkius, bet ir standartinius nuokrypius, medianas, min/max reikšmes
   - Naudoti statistinius testus algoritmo veikimo įvertinimui

5. **Vizualizacijų tobulinimas**:
   - Sukurti interaktyvius grafikus, kurie leistų dinamiškai keisti parametrus
   - Pridėti tikslesnį eksponentinės ir polinominės augimo funkcijų palyginimą
   - Vizualizuoti skirtingų algoritmų veikimo principus (pvz., backtracking medžio vizualizacija)

6. **Rekomendacijos dideliems duomenims**:
   - Ištirti, kaip spręsti NP-pilnas problemas su dideliais duomenų rinkiniais (n > 1000)
   - Sukurti euristikas ir aproksimacijas, kurios suteiktų pakankamai gerus rezultatus praktiniams atvejams
   - Palyginti euristikų ir tikslių algoritmų rezultatų kokybę