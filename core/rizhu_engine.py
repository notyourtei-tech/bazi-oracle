from core.constants import GAN_WUXING

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
