import pygame
import random
import sys
sys.setrecursionlimit(2000)


GENISLIK = 800
YUKSEKLIK = 800


SIYAH = (0, 0, 0)
YESIL = (0, 255, 0)


YILAN_BOYUTU = 20


FPS = 100000


pygame.init()


tahta = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Yılan Oyunu")


fps_kontrol = pygame.time.Clock()


yilan_baslangic_x = GENISLIK // 2
yilan_baslangic_y = YUKSEKLIK // 2


yilan_hizi_x = 0
yilan_hizi_y = YILAN_BOYUTU


yilan_vucut = []
yilan_uzunlugu = 1



yem_x = round(random.randrange(0, GENISLIK - YILAN_BOYUTU) / 20.0) * 20.0
yem_y = round(random.randrange(0, YUKSEKLIK - YILAN_BOYUTU) / 20.0) * 20.0


yol_stack = []



def dfs(yilan_bas_x, yilan_bas_y, hedef_x, hedef_y, ziyaret_edilen):
    if (yilan_bas_x, yilan_bas_y) == (hedef_x, hedef_y):
        return True

    ziyaret_edilen.add((yilan_bas_x, yilan_bas_y))
    hareketler = [(YILAN_BOYUTU, 0), (-YILAN_BOYUTU, 0), (0, YILAN_BOYUTU), (0, -YILAN_BOYUTU)]

    for hareket in hareketler:
        yeni_x = yilan_bas_x + hareket[0]
        yeni_y = yilan_bas_y + hareket[1]

        if yeni_x >= GENISLIK or yeni_x < 0 or yeni_y >= YUKSEKLIK or yeni_y < 0:
            continue

        if (yeni_x, yeni_y) in yilan_vucut:
            continue

        if (yeni_x, yeni_y) in ziyaret_edilen:
            continue

        if dfs(yeni_x, yeni_y, hedef_x, hedef_y, ziyaret_edilen):
            yol_stack.append((hareket[0], hareket[1]))
            return True

    return False




def yilan_hareket():
    global yilan_baslangic_x, yilan_baslangic_y, yilan_hizi_x, yilan_hizi_y

    if not yol_stack:
        dfs(yilan_baslangic_x, yilan_baslangic_y, yem_x, yem_y, set())

    if yol_stack:
        hareket = yol_stack.pop()
        yilan_hizi_x, yilan_hizi_y = hareket[0], hareket[1]

    yilan_baslangic_x += yilan_hizi_x
    yilan_baslangic_y += yilan_hizi_y


skor = 0


font = pygame.font.Font(None, 36)


skor_metni = font.render("Skor: " + str(skor), True, YESIL)


def skor_goster():
    tahta.blit(skor_metni, (10, 10))



oyun_devam_ediyor = True
while oyun_devam_ediyor:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            oyun_devam_ediyor = False


    yilan_hareket()



    if yilan_baslangic_x >= GENISLIK or yilan_baslangic_x < 0 or yilan_baslangic_y >= YUKSEKLIK or yilan_baslangic_y < 0:
        oyun_devam_ediyor = True


    if yilan_baslangic_x == yem_x and yilan_baslangic_y == yem_y:
        yem_x = round(random.randrange(0, GENISLIK - YILAN_BOYUTU) / 20.0) * 20.0
        yem_y = round(random.randrange(0, YUKSEKLIK - YILAN_BOYUTU) / 20.0) * 20.0
        yilan_uzunlugu += 1
        skor += 1
        skor_metni = font.render("Skor: " + str(skor), True, YESIL)

    if skor > (GENISLIK * YUKSEKLIK) / 2000:
        oyun_devam_ediyor = False

    tahta.fill(SIYAH)
    skor_goster()


    yilan_bas = []
    yilan_bas.append(yilan_baslangic_x)
    yilan_bas.append(yilan_baslangic_y)
    yilan_vucut.append(yilan_bas)
    if len(yilan_vucut) > yilan_uzunlugu:
        del yilan_vucut[0]


    for segment in yilan_vucut[:-1]:
        if segment == yilan_bas:
            oyun_devam_ediyor = True


    for segment in yilan_vucut:
        pygame.draw.rect(tahta, YESIL, [segment[0], segment[1], YILAN_BOYUTU, YILAN_BOYUTU])


    pygame.draw.rect(tahta, YESIL, [yem_x, yem_y, YILAN_BOYUTU, YILAN_BOYUTU])


    pygame.display.update()


    fps_kontrol.tick(FPS)


pygame.quit()