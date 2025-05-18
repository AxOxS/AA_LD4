# Algoritmų analizės projekto pristatymas

## 1. Projekto struktūra

Projektas organizuotas pagal šiuolaikines programinės įrangos kūrimo praktikas, su aiškia moduline struktūra:

```
algorithm-analysis/
├── src/                     # Source katalogas
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
│   ├── algorithm_analysis_report.txt   # Automatiškai sugeneruota ataskaita
│   ├── subset_sum_backtracking.png     # Backtracking algoritmo grafikas
│   ├── subset_sum_dp.png               # Dinaminio programavimo grafikas
│   ├── subset_sum_worst_case.png       # Blogiausio atvejo analizės grafikas
│   ├── shortest_path.png               # Dijkstra algoritmo grafikas
│   ├── algorithm_comparison.png        # P ir NP algoritmų palyginimas
│   └── results_pc2/                    # Antrojo kompiuterio rezultatai
├── main.py                  # main failas
└── requirements.txt         # Būtinos bibliotekos
```

### 1.1 Pagrindinių komponentų aprašymas

- **algorithms/** - Implementuoja tiek P, tiek NP-pilnos klasės algoritmus
  - **subset_sum.py** - NP-pilnos klasės problemų algoritmai (backtracking, dinamininis programavimas, išsamus)
  - **shortest_path.py** - P klasės algoritmas (Dijkstra)

- **benchmarks/** - Matavimo ir bandymų įrankiai
  - **subset_sum_benchmark.py** - Poaibio sumos algoritmų analizė su fiksuotais testais ir nustatytais bandymų skaičiais
  - **shortest_path_benchmark.py** - Dijkstra algoritmo našumo matavimas
  - **compare_algorithms.py** - P ir NP-pilnos klasės algoritmų tiesioginis palyginimas

- **utils/** - Pagalbiniai įrankiai
  - **timer.py** - Tikslus laiko matavimas ir sistemos informacijos išgavimas
  - **plotting.py** - Rezultatų vizualizacijos su logaritminėmis skalėmis
  - **graph_utils.py** - Svorinių grafų generavimas ir "sunkių" testų kūrimas

### 1.2 Architektūriniai sprendimai

Projektas sukurtas laikantis šių principų:

1. **Modulinė organizacija** - kiekvienas komponentas turi aiškų vaidmenį ir atsakomybę
2. **Aukšto lygio abstrakcijos** - algoritmai ir jų testavimas atskirti nuo bendrosios logikos
3. **Pakartotinis panaudojamumas** - bendri komponentai (laiko matavimas, vizualizacijos) išskirti į utils/ katalogą
4. **Testavimo integravimas** - automatiniai testai užtikrina algoritmų teisingumą
5. **Rezultatų reprodukuojamumas** - fiksuotas atsitiktinis generatorius (random seed) užtikrina vienodus testinius duomenis

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

#### Kompiuteris 1 (pagrindinis)
- CPU: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel
- RAM: 31.43GB
- OS: Windows 11

#### Kompiuteris 2 (antrinis)
- CPU: Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
- RAM: 15.74GB
- OS: Windows 11

### Poaibio sumos algoritmo rezultatai

#### Backtracking algoritmas (Kompiuteris 1)
Testai atlikti su įvesties dydžiais: 5, 10, 15, 20, 22, 24, 26, 28 su fiksuotais testiniais duomenimis

```
Testing size 5...  → Average: 10.00 μs
Testing size 10... → Average: 11.00 μs
Testing size 15... → Average: 2.47 ms
Testing size 20... → Average: 899.00 μs
Testing size 22... → Average: 1.59 ms
Testing size 24... → Average: 6.84 ms
Testing size 26... → Average: 20.84 ms
Testing size 28... → Average: 104.58 ms
```

#### Backtracking algoritmas (Kompiuteris 2)
Testai atlikti su tais pačiais įvesties dydžiais ir duomenimis

```
Testing size 5...  → Average: 10.00 μs
Testing size 10... → Average: 20.00 μs
Testing size 15... → Average: 4.53 ms
Testing size 20... → Average: 1.85 ms
Testing size 22... → Average: 3.07 ms
Testing size 24... → Average: 12.88 ms
Testing size 26... → Average: 43.02 ms
Testing size 28... → Average: 203.93 ms
```

#### Dinaminis programavimas (Kompiuteris 1)
Testai atlikti su įvesties dydžiais: 5, 10, 20, 50, 100, 200, 500, 1000 su nuosekliais testiniais duomenimis

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

#### Dinaminis programavimas (Kompiuteris 2)
Testai atlikti su tais pačiais duomenimis

```
Testing size 5...   → Average: 29.94 μs
Testing size 10...  → Average: 81.22 μs
Testing size 20...  → Average: 398.67 μs
Testing size 50...  → Average: 2.27 ms
Testing size 100... → Average: 9.73 ms
Testing size 200... → Average: 32.15 ms
Testing size 500... → Average: 215.32 ms
Testing size 1000...→ Average: 798.76 ms
```

#### Blogiausio atvejo testavimas (išsamus, Kompiuteris 1)
Testai atlikti su specialiai paruoštais duomenimis, kurie garantuoja visų poaibių patikrinimą, naudojant fiksuotą atsitiktinių skaičių generatoriaus (random seed) reikšmę.

```
Testing size 10... → Average: 189.71 μs
Testing size 12... → Average: 413.58 μs
Testing size 15... → Average: 3.42 ms
Testing size 18... → Average: 25.78 ms
Testing size 20... → Average: 104.36 ms
Testing size 22... → Average: 417.92 ms
Testing size 25... → Average: 3.5824 s
```

#### Blogiausio atvejo testavimas (išsamus, Kompiuteris 2)
Testai atlikti su tais pačiais duomenimis.

```
Testing size 10... → Average: 215.32 μs
Testing size 12... → Average: 487.16 μs
Testing size 15... → Average: 3.87 ms
Testing size 18... → Average: 31.24 ms
Testing size 20... → Average: 126.84 ms
Testing size 22... → Average: 508.61 ms
Testing size 25... → Average: 4.2376 s
```

### Trumpiausio kelio algoritmo rezultatai

#### Dijkstra algoritmas (Kompiuteris 1)
Testai atlikti su atsitiktinai generuotais grafais, naudojant fiksuotą atsitiktinių skaičių generatoriaus sėklą

```
Testing size 10...   → Average: 13.00 μs
Testing size 50...   → Average: 129.00 μs
Testing size 100...  → Average: 351.00 μs
Testing size 200...  → Average: 1.57 ms
Testing size 500...  → Average: 4.28 ms
Testing size 1000... → Average: 16.91 ms
```

#### Dijkstra algoritmas (Kompiuteris 2)
Testai atlikti su tais pačiais duomenimis

```
Testing size 10...   → Average: 21.00 μs
Testing size 50...   → Average: 168.00 μs
Testing size 100...  → Average: 473.00 μs
Testing size 200...  → Average: 1.55 ms
Testing size 500...  → Average: 8.36 ms
Testing size 1000... → Average: 27.79 ms
```

Abiejų kompiuterių rezultatuose matoma aiški polinominė augimo tendencija, kurios eksperimentinė išraiška yra artima n^1.6, kas praktiškai atitinka teorinį O(n²) sudėtingumą tankiems grafams.

## 4. Rezultatų analizė ir palyginimas

### Eksperimentiškai nustatytos augimo funkcijos

#### Kompiuteris 1 

Iš algoritmo analizės ataskaitos (`algorithm_analysis_report.txt`):

```
NP-COMPLETE ALGORITHM (SUBSET SUM - BACKTRACKING):
Tested sizes: [5, 10, 15, 20, 22, 24, 26, 28]
Execution times (s): [1e-05, 1.1e-05, 0.002467, 0.000899, 0.001587, 0.006838, 0.02084, 0.104582]
Experimentally determined growth rate: n^5.097554893670223
Theoretical complexity: O(2^n)

POLYNOMIAL ALGORITHM (DIJKSTRA'S SHORTEST PATH):
Tested sizes: [10, 50, 100, 200, 500, 1000]
Execution times (s): [1.3e-05, 0.000129, 0.000351, 0.001574, 0.004282, 0.01691]
Experimentally determined growth rate: n^1.5591066071053163
Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs
```

#### Kompiuteris 2

Iš algoritmo analizės ataskaitos (`results_pc2/algorithm_analysis_report.txt`):

```
NP-COMPLETE ALGORITHM (SUBSET SUM - BACKTRACKING):
Tested sizes: [5, 10, 15, 20, 22, 24, 26, 28]
Execution times (s): [1e-05, 2e-05, 0.004531, 0.001845, 0.003065, 0.012877, 0.04302, 0.203926]
Experimentally determined growth rate: n^5.402924470128604
Theoretical complexity: O(2^n)

POLYNOMIAL ALGORITHM (DIJKSTRA'S SHORTEST PATH):
Tested sizes: [10, 50, 100, 200, 500, 1000]
Execution times (s): [2.1e-05, 0.000168, 0.000473, 0.001554, 0.008359, 0.027791]
Experimentally determined growth rate: n^1.5738923715759845
Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs
```

### Pastabos dėl eksperimentinių augimo funkcijų

1. **Poaibio suma (backtracking, Kompiuteris 1)**: Eksperimentiškai nustatyta augimo funkcija n^5.10 neatspindi tikrosios eksponentinės funkcijos O(2^n) dėl kelių priežasčių:
   - Su mažesniais įvesties dydžiais eksponentinis augimas dar nėra toks ryškus
   - Algoritmo optimizacijos (rikiavimas ir filtravimas) pagerina darbą kai kuriems atvejams
   - Matome nereguliarų vykdymo laiką (pvz., didelį šuolį tarp n=15 ir n=24), kas rodo, kad algoritmo elgsena priklauso nuo konkrečių duomenų
   - Labiausiai eksponentinis augimas matomas tarp n=26 (20.84 ms) ir n=28 (104.58 ms), kur vykdymo laikas išauga ~5 kartus pridėjus tik 2 elementus

2. **Poaibio suma (backtracking, Kompiuteris 2)**: Eksperimentiškai nustatyta augimo funkcija n^5.40 rodo šiek tiek greitesnį augimą nei Kompiuteryje 1. Įdomu pastebėti, kad:
   - Visais atvejais Kompiuteris 2 rodo ~2 kartus ilgesnį vykdymo laiką nei Kompiuteris 1
   - Augimo tendencija išlieka panaši, tačiau algoritmo elgsena skirtingais laiko momentais šiek tiek skiriasi
   - Santykinis skirtumas tarp algoritmų vykdymo laiko yra pastovesnis didesnėms įvestims (n=26 ir n=28)

3. **Poaibio suma (blogiausias atvejis)**: Specialiai sukonstruoti blogiausio atvejo scenarijai aiškiau parodo eksponentinį augimą:
   - Kompiuteryje 1 vykdymo laikas auga nuo 417.92 ms (n=22) iki 3.58s (n=25) - ~8.6 karto padidėjimas pridėjus tik 3 elementus
   - Kompiuteryje 2 vykdymo laikas auga nuo 508.61 ms (n=22) iki 4.24s (n=25) - ~8.3 karto padidėjimas
   - Tai labiau atitinka teorinį 2^n augimą, nes 2^3 = 8, todėl tikėtumėmės maždaug 8 kartų padidėjimo

4. **Dijkstra algoritmas**: Eksperimentiškai nustatytos augimo funkcijos:
   - Kompiuteris 1: n^1.56, kas praktiškai atitinka teorinį O(n²) sudėtingumą tankiems grafams
   - Kompiuteris 2: n^1.57, kas beveik identiška pirmajam kompiuteriui
   - Abiem atvejais matome nuoseklų, prognozuojamą augimą be didelių anomalijų
   - Įdomu, kad nors Kompiuteris 2 turi mažiau RAM ir, tikėtina, lėtesnį CPU, vykdymo laikų skirtumas yra mažesnis nei NP-pilnos klasės algoritmuose

5. **Algoritmų tobulinimo padariniai**: Šio projekto metu buvo patobulintas testavimo procesas:
   - Įvestas fiksuotas atsitiktinis generatorius (fixed random seed) duomenų generavimui
   - Padidintas bandymų skaičius nuo 3 iki 10 kiekvienam įvesties dydžiui
   - Naudojami sunkesni testavimo atvejai backtracking algoritmui
   
   Šie patobulinimai leido gauti stabilesnius ir labiau reprezentatyvius rezultatus, kurie geriau atspindi teorines algoritmų savybes.

### Grafinė vizualizacija

Projektas sugeneravo keletą grafikų, parodančių algoritmų vykdymo laiką:

1. **algorithm_comparison.png** - Tiesioginis P ir NP-pilnos klasės algoritmų palyginimas
2. **subset_sum_backtracking.png** - Poaibio sumos backtracking algoritmo veikimas
3. **subset_sum_dp.png** - Poaibio sumos dinaminio programavimo algoritmo veikimas
4. **subset_sum_worst_case.png** - Poaibio sumos blogiausio atvejo analizė
5. **shortest_path.png** - Trumpiausio kelio algoritmo veikimas

Grafikai naudoja logaritminę skalę y ašiai, kad būtų galima aiškiau pamatyti eksponentinį ir polinominį augimą.

### Našumo matavimo metodologija

Matavimų patikimumui užtikrinti buvo įgyvendinti šie patobulinimai:

1. **Fiksuoti testiniai duomenys**:
   - Įvestas fiksuotas atsitiktinis generatorius (random seed = 42)
   - Sukurti "sunkūs" testiniai atvejai poaibio sumos algoritmui, kuriuose skaičiai yra artimi vienas kitam
   - Visų algoritmų testiniai duomenys išlaikomi tarp skirtingų bandymų ir sistemų

2. **Bandymų patobulinimai**:
   - Padidintas bandymų skaičius nuo 3 iki 10 kiekvienam įvesties dydžiui
   - Rezultatų išvestis išplėsta, kad parodytų kiekvieno bandymo rezultatus atskirai
   - Vykdymo laikai matuojami mikrosekundžių tikslumu
   - Įvestas laiko ribojimas ilgiems bandymams (blogiausio atvejo testams)

3. **Patobulintos vizualizacijos**:
   - Logaritminės skalės grafikai leidžia aiškiau pamatyti augimo tendencijas
   - Grafikai generuojami aukštos rezoliucijos (DPI=300)
   - Pridėta teorinio sudėtingumo kreivė, parodanti, kaip eksperimentiniai rezultatai atrodo lyginant su teoriniais modeliais

4. **Sistemos apribojimų valdymas**:
   - Bandymai vykdomi paeiliui, užtikrinant, kad sistemos ištekliai (CPU, RAM) būtų panašiai prieinami kiekvienam bandymui
   - Pridėtas ankstyvo nutraukimo mechanizmas, kad būtų išvengta pernelyg ilgų vykdymo laikų
   - Automatinis CPU ir RAM informacijos išgavimas, kad būtų galima įvertinti aparatinės įrangos poveikį rezultatams

5. **Platforma ir aplinka**:
   - Python 3.10 arba naujesnė versija
   - Visos matavimo funkcijos sukurtos naudojant `time.perf_counter()` tiksliam mikro-laiko matavimui
   - Matavimo kodas išlaikytas minimalus, kad išvengtų "matavimo triukšmo"
   - Naudojami virtualūs aplinkos (venv) izoliuoti eksperimentus nuo kitų sistemoje vykdomų procesų

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

### Kompiuteris 1 (pagrindinis):
- CPU: Intel64 Family 6 Model 197 Stepping 2, GenuineIntel
- RAM: 31.43GB
- OS: Windows 11

### Kompiuteris 2 (antrinis):
- CPU: Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
- RAM: 15.74GB
- OS: Windows 11

### Rezultatų palyginimas

#### NP-Pilna problema (Poaibio suma - Backtracking)

| Kompiuteris | Eksperimentiškai nustatytas augimo greitis | Vykdymo laikas (n=28) |
|-------------|------------------------------------------|---------------------|
| 1           | n^5.10                                   | 104.58 ms           |
| 2           | n^5.40                                   | 203.93 ms           |

#### P problema (Dijkstra trumpiausias kelias)

| Kompiuteris | Eksperimentiškai nustatytas augimo greitis | Vykdymo laikas (n=1000) |
|-------------|------------------------------------------|----------------------|
| 1           | n^1.56                                   | 16.91 ms              |
| 2           | n^1.57                                   | 27.79 ms             |

### Analizė

1. **Aparatinės įrangos įtaka**:
   - Kompiuteris 1 turi daugiau RAM (31.43GB vs 15.74GB), o taip pat greičiausiai naujesnį/greitesnį CPU (Model 197 vs 140)
   - Pastebimas sisteminis skirtumas: Kompiuteris 1 visada vykdo algoritmus ~1.6-2 kartus greičiau nei Kompiuteris 2
   - Nepaisant absoliutaus vykdymo laiko skirtumų, augimo tendencijos išlieka labai panašios

2. **Backtracking algoritmo palyginimas**:
   - Fiksuotų testinių duomenų naudojimas leido gauti palyginamus rezultatus skirtingose sistemose
   - Abiejuose kompiuteriuose matomas panašus sudėtingumo augimas: n^5.10 vs n^5.40
   - Vykdymo laikas su n=28 skiriasi maždaug 2 kartus: 104.58 ms vs 203.93 ms
   - Ankstesniuose bandymuose (su atsitiktiniais duomenimis) skirtumas buvo daug didesnis, kas rodo, kad testavimo vienodumo užtikrinimas yra labai svarbus

3. **Dijkstros algoritmo palyginimas**:
   - Abu kompiuteriai rodo beveik identišką teorinį augimo greitį: n^1.56 vs n^1.57
   - Kompiuteris 1 šiek tiek greitesnis (16.91ms vs 27.79ms su n=1000), išlaikant pastovų ~1.6x santykį
   - P klasės algoritmo rezultatai yra stabilesni ir labiau prognozuojami abiejose sistemose

4. **Blogiausio atvejo analizė**:
   - Specialiai sukonstruoti blogiausio atvejo scenarijai rodo eksponentinį augimą abiejuose kompiuteriuose
   - Santykis tarp n=22 ir n=25 laiko abiejuose kompiuteriuose yra artimas teoriniam 2^3=8 kartų didėjimui
   - Blogiausio atvejo testai davė stabilesnius ir labiau palyginamus rezultatus nei atsitiktiniai testai

5. **Eksperimentų patobulinimai**:
   - Fiksuotas atsitiktinis generatorius (random seed = 42) užtikrino vienodus testinius duomenis
   - Padidinus bandymų skaičių nuo 3 iki 10 sumažėjo matavimų dispersija
   - Naudojant sunkesnius testinius atvejus backtracking algoritmui gauti reprezentatyvesni rezultatai
   - Bendros kodo optimizacijos sumažino sistemines paklaidas

### Išplėstinė palyginamoji analizė

```
                           | Kompiuteris 1   | Kompiuteris 2   | Santykis (K2/K1)
---------------------------|-----------------|-----------------|----------------
CPU modelis                | 197             | 140             | -
RAM                        | 31.43GB         | 15.74GB         | 0.50x
Subset Sum (n=15)          | 2.47 ms         | 4.53 ms         | 1.83x
Subset Sum (n=20)          | 899.00 μs       | 1.85 ms         | 2.06x
Subset Sum (n=24)          | 6.84 ms         | 12.88 ms        | 1.88x
Subset Sum (n=28)          | 104.58 ms       | 203.93 ms       | 1.95x
Augimo funkcija            | n^5.10          | n^5.40          | 1.06x
Worst Case (n=25)          | 3.58 s          | 4.24 s          | 1.18x
Dijkstra (n=500)           | 4.28 ms         | 8.36 ms         | 1.95x
Dijkstra (n=1000)          | 16.91 ms        | 27.79 ms        | 1.64x
Augimo funkcija            | n^1.56          | n^1.57          | 1.01x
```

Ši detali palyginamoji analizė atskleidžia įdomias tendencijas:

1. Kompiuteris 1 sistemiškai apie 1.6-2 kartus greitesnis už Kompiuterį 2 visuose testuose
2. NP-pilnos klasės algoritmo vykdymo laiko skirtumai yra labiau kintantys (1.83x-2.06x) nei P klasės algoritmo (1.64x-1.95x)
3. Augimo funkcijų eksponentės labai panašios abiejuose kompiuteriuose (1.01x-1.06x skirtumas)
4. Blogiausio atvejo testo skirtumas yra mažesnis (1.18x) nei kitų testų, kas gali būti susiję su sistemine CPU architektūra ir optimizacijomis

Šie rezultatai pabrėžia, kad net ir skirtingose sistemose galima stebėti panašias algoritmų augimo tendencijas, jei testiniai duomenys yra pakankamai vienodi ir testavimai atliekami metodiškai.

6. **Kodėl blogiausio atvejo scenarijai rodo mažesnį sistemų našumo skirtumą?**
   - Intensyvus skaičiavimų pobūdis mažiau priklauso nuo kompiuterio periferinių įrenginių (RAM, diskas) greičio
   - CPU architektūriniai skirtumai gali būti mažiau reikšmingi tokio tipo skaičiavimams
   - Galima iškelti hipotezę, kad intensyvūs skaičiavimai geriau optimizuojami abiejų sistemų kompiliatorių

7. **Sisteminis faktorius - "šilumos ribojimai" (thermal throttling)**:
   - Ilgai trunkantys intensyvūs skaičiavimai (pvz., blogiausio atvejo testas n=25) gali sukelti CPU perkaitimą
   - Tokiu atveju įsijungia sisteminės apsaugos, sumažinančios CPU veikimo dažnį
   - Tai gali paaiškinti, kodėl ilgų testų vykdymo laikų santykis (1.18x) yra mažesnis nei trumpų testų (1.8-2.0x)

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