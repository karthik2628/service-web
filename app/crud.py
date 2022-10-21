from . import db, models, util


def get_password(username: str, role: str) -> str:
    if role == "admin":
        password = models.Admin.query.filter_by(username=username).first()
    else:
        password = models.Technician.query.filter_by(username=username).first()

    if password:
        return password.password
    else:
        return None


def create_admin(data: dict) -> None:
    errors = ""
    if util.is_username_available(data["username"], "admin"):
        errors = "Username already exists,"

    if errors:
        raise Exception(errors)

    user = models.Admin(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()


def create_technician(data: dict) -> None:
    errors = ""
    if util.is_username_available(data["username"], "technician"):
        errors = "Username already exists"

    if errors:
        raise Exception(errors)

    user = models.Technician(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()


def get_all_technicians() -> list:
    technicians = models.Technician.query.all()
    return technicians


def get_all_admins() -> list:
    admins = models.Admin.query.all()
    return admins

def get_all_onsitetasks(filter: dict = None) -> list:
    tasks = models.OnsiteTask.query
    if filter:
        customer = get_customer_by_phone(filter["fphone"])
        if customer:
            customer_id = customer.customer_id
            tasks = tasks.filter_by(customer_id=customer_id)
        if filter["fid"]:
            tasks = tasks.filter_by(task_id=filter["fid"])
        if filter["fdate"]:
            tasks = tasks.filter_by(date=filter["fdate"])
        if get_technician_id_by_name(filter["ftechnician"]):
            tasks = tasks.filter_by(technician_id=get_technician_id_by_name(filter["ftechnician"]))
    tasks = tasks.all()
    return tasks

def get_technician_id_by_name(name: str) -> int:
    technician = models.Technician.query.filter_by(name=name).first()
    if(technician):
        return techician.technician_id
    else:
        return None

def get_onsitetask_by_id(task_id) -> models.OnsiteTask:
    return models.OnsiteTask.query.filter_by(task_id=task_id).first()

def update_onsitetasks(data) -> list:
    if util.is_task_available(data['task_id']):
        task_id = data.pop('task_id')
        db.session.query(models.Resources).filter(models.Resources.task_id == task_id).update(data)
        db.session.commit()
        db.session.flush()
    else:
        update_tasks=models.Resources(**data)
        db.session.add(update_tasks)
        db.session.commit()
        db.session.flush()


def get_resources_by_id(task_id: int) -> models.Resources:
    return models.Resources.query.filter_by(task_id=task_id).first()

def get_admin(username: str) -> models.Admin:
    return models.Admin.query.filter_by(username=username).first()


def get_technician(username: str) -> models.Technician:
    return models.Technician.query.filter_by(username=username).first()


def create_task(data: dict) -> None:
    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
            "address": data.pop("address"),
        }
    )

    if not util.is_customer_available(customer_data["phone_no"]):
        create_customer(customer_data)
    data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id

    task = models.OnsiteTask(**data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()


def instore_task(data: dict) -> None:
    customer_data = {}
    customer_data.update(
        {
            "name": data.pop("customer_name"),
            "phone_no": data.pop("phone_no"),
            
        }
    )

    if not util.is_customer_available(customer_data["phone_no"]):
        create_customer(customer_data)
    data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id

    product_detail = {}
    product_detail.update(
        {
            "product_name": data.pop("product_name"),
            "product_company": data.pop("product_company")
        }
    )

    
    if not util.is_product_available(product_detail['product_name']):
        create_product(product_detail)
    data["product_id"] = get_product(product_detail["product_name"]).product_id

    

    task = models.InstoreTask(**data)
    db.session.add(task)
    db.session.commit()
    db.session.flush()

def get_all_instoretasks() -> list:
    tasks = models.InstoreTask.query.all()
    return tasks

def get_instoretask_by_id(in_task_id) -> models.InstoreTask:
    return models.InstoreTask.query.filter_by(in_task_id=in_task_id).first()


def update_instoretasks(data) -> list:
    if util.is_instore_task_available(data['in_task_id']):
        
        customer_data = {}
        customer_data.update(
            {
                "name": data.pop("customer_name"),
                "phone_no": data.pop("phone_no"),
                
            }
        )

        if not util.is_customer_available(customer_data["phone_no"]):
            create_customer(customer_data)
        data["customer_id"] = get_customer_by_phone(customer_data["phone_no"]).customer_id

        product_detail = {}
        product_detail.update(
            {
                "product_name": data.pop("product_name"),
                "product_company": data.pop("product_company")
            }
        )


        if not util.is_product_available(product_detail['product_name']):
            create_product(product_detail)
        data["product_id"] = get_product(product_detail["product_name"]).product_id




        in_task_id = data.pop('in_task_id')
        db.session.query(models.InstoreTask).filter(models.InstoreTask.in_task_id == in_task_id).update(data)
        db.session.commit()
        db.session.flush()
    else:
        update_tasks=models.InstoreTask(**data)
        db.session.add(update_tasks)
        db.session.commit()
        db.session.flush()



def get_customer_by_phone(phone_no: str) -> models.Customer:
    return models.Customer.query.filter_by(phone_no=phone_no).first()


def create_customer(data: dict) -> None:
    if util.is_customer_available(data["phone_no"]):
        print("hello")

    user = models.Customer(**data)
    db.session.add(user)
    db.session.commit()
    db.session.flush()

def get_all_customer()-> list:
    customers = models.Customer.query.all()
    return customers


def get_product(product_name: str) -> models.Products:
    return models.Products.query.filter_by(product_name=product_name).first()

def create_product(data: dict) -> None:
    if util.is_product_available(data['product_name']):
        print("hello")
    print(data)
    
    product = models.Products(**data)
    db.session.add(product)
    db.session.commit()
    db.session.flush()