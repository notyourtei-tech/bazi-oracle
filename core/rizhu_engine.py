GAN_WUXING = {
    "甲": "wood", "乙": "wood",
    "丙": "fire", "丁": "fire",
    "戊": "earth", "己": "earth",
    "庚": "metal", "辛": "metal",
    "壬": "water", "癸": "water",
}

def build_rizhu(bazi: dict):
    """
    日主 = 日干
    """
    day_gan = bazi["day"][0]
    wuxing = GAN_WUXING.get(day_gan)

    return {
        "gan": day_gan,
        "wuxing": wuxing
    }
