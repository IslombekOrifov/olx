

def upload_category_path(instance, image):
    return f"categories/{instance.name}/{image}"


def upload_product_path(instanse, image):
    return f"products/{instanse.title}/{image}"