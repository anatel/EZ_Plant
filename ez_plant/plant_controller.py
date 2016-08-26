from ez_plant.user import User

class PlantController(object):
    def __init__(self, user):
        self.user = user

    def create_plant(self, m_port, w_port, plant_type, plant_name, water_data, image_url):
        new_plant = self.user.add_plant(m_port, int(w_port), plant_type, plant_name, water_data, image_url)
        return self.jsonify_plant(new_plant)

    def update_plant(self, plant_id, m_port, w_port, plant_type, plant_name, water_data, image_url):
        updated_plant = self.user.update_plant(plant_id, m_port, int(w_port), plant_type, plant_name, water_data, image_url)
        return self.jsonify_plant(updated_plant)

    def jsonify_plant(self, plant):
        plant_json = vars(plant)

        return plant_json
