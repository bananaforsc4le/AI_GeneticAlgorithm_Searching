import random
import math
import copy


#GA for searching, blom learning
#binary population
#pakai biner

def buat_populasi(ukuran): #inisialisasi populasi
    new_pop_baris = [] #banyak gen 8
    new_pop_kol = []
    i = 0
    while (i < ukuran):
        j = 0
        while (j < 8):
            new_pop_kol.append(random.randint(0,1))
            j = j+1
        new_pop_baris.append(new_pop_kol)
        new_pop_kol = []
        i = i+1

    return new_pop_baris #output populasi

def dekode_kromosom(arr_krom): #dekode kromosom
    hasil = [1]

    hasil[0] = -3 + 3 - 3 / (math.pow(2, -1) + math.pow(2, -2) + math.pow(2, -3) + math.pow(2, -4)) * ((arr_krom[0] * math.pow(2, -1)) + (arr_krom[1] * math.pow(2, -2)) + (arr_krom[2] * math.pow(2, -3)) + (arr_krom[3] * math.pow(2, -4)))
    hasil.append(-2 + 2 - 2 / (math.pow(2, -1) + math.pow(2, -2) + math.pow(2, -3) + math.pow(2, -4)) * ((arr_krom[4] * math.pow(2, -1)) + (arr_krom[5] * math.pow(2, -2)) + (arr_krom[6] * math.pow(2, -3)) + (arr_krom[7] * math.pow(2, -4))))

    return hasil #ouput hasil dekode

def f_objektif(hasil_dekode): #nilai fungsi objektif
    x1 = hasil_dekode[0]
    x2 = hasil_dekode[1]

    hasil_f = (4 - 2.1 * math.pow(x1,2) + math.pow(x1,4)/3) * math.pow(x1,2) + x1 * x2 + (-4 + 4 * math.pow(x2,2) * math.pow(x2,2))

    return hasil_f #output hasil fungsi objektif


def fitness(arr_pop = []): #input populasi
    fit = []
    i = 0
    while (i < len(arr_pop)):
        dekode = dekode_kromosom(arr_pop[i])
        obj = f_objektif(dekode)
        fit.append(1/obj+0.01)
        i = i+1
    return fit #output, fitness per individu


def seleksi_parent(arr_pop=[],fitness=[]):
    prop = [] #list untuk hitung proporsi
    parent = [] # 2 parent


    tot_fitness = sum(fitness) #total fitness

    i = 0
    while (i<len(arr_pop)):
        prop.append(fitness[i]/tot_fitness)
        i = i+1

    j = 0 #dua parent
    while (j<2):
        random_num = random.uniform(0,1)
        current_prop = 0 #total proporsi saat ini
        k = 0
        while (current_prop<random_num):
            current_prop += prop[k]
            k = k + 1
        parent.append(arr_pop[k-1])
        j=j+1

    return parent

def crossover(parent=[]):
    #probabilitas crossover random
    child_baris = []
    child_kolom = []
    prob_cross = round(random.uniform(0,1),1) #random probabilitas range 0-1, 1 angka dibelakang koma
    random_num= random.uniform(0,1)
    if (random_num < prob_cross):
        child = parent.copy()
        titik_potong = random.randint(1,7)
        #child_kolom.append(parent.copy())#child 1
        #child_kolom.append(parent.copy())#child 2
        i = 0
        while (i != titik_potong and i < 8):
            child[0][titik_potong] = parent[1][titik_potong]
            child[1][titik_potong] = parent[0][titik_potong]
            print (titik_potong)
            i = i+1
        return child

    else:
        return parent

def mutasi(child=[]):
    prob_mutasi = round(random.uniform(0,1),1)
    i= 0
    j=0
    while(j<2):
        while (i<len(child)):
            random_num = random.uniform(0,1)
            if (random_num < prob_mutasi):
                child[j][i] = random.randint(0,1)
            i = i+1
        j=j+2
    return child


def fit_rendah(fit=[]):#mencari fitness terendah
    curr_fit = fit[0]
    i = 0
    j=0
    while (i<len(fit)):
        if curr_fit > fit[i]:
            curr_fit = fit[i]
            j = i
        i = i+1
    return j

def best_fit(fit=[]):
    curr_fit = fit[0]
    i = 0
    j = 0
    while (i < len(fit)):
        if curr_fit < fit[i]:
            curr_fit = fit[i]
            j = i
        i = i + 1
    return j

def generational_replace(child = [], pop_lama=[],fit=[]):#fitness terendah akan digantikan; child hasil cross
    pop_baru = pop_lama.copy()

    fit_terendah = fit_rendah(fit)

    pop_baru[fit_terendah]= child[0];

    return pop_baru



if __name__ == "__main__":
    set_populasi = 10
    generasi = 1000

    i = 0
    populasi = buat_populasi(set_populasi)

    while (i < generasi):
        fit = fitness(populasi)
        get_best = best_fit(fit)
        parent_select = seleksi_parent(populasi,fit)
        child = crossover(parent_select)
        populasi = generational_replace(child,populasi,populasi)
        i = i + 1

    print("generasi ke- ",i)
    print(populasi)
    f_minimal = dekode_kromosom(populasi[get_best])
    hasil_f = f_objektif(f_minimal)
    print("X dan Y", f_minimal)
    print("Hasil fungsi: ",hasil_f)
