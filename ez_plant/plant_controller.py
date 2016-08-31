import datetime

class PlantController(object):
    def __init__(self, user):
        self.user = user

    def create_plant(self, m_port, w_port, plant_type, plant_name, water_data, image_dir, image_type):
        new_plant = self.user.add_plant(m_port, int(w_port), plant_type, plant_name, water_data, image_dir, image_type)
        return self.jsonify_plant(new_plant)

    def update_plant(self, plant_id, m_port, w_port, plant_type, plant_name, water_data, image_dir, image_type):
        updated_plant = self.user.update_plant(plant_id, m_port, int(w_port), plant_type, plant_name, water_data, image_dir, image_type)
        return self.jsonify_plant(updated_plant)

    def delete_plant(self, plant_id):
        self.user.delete_plant(plant_id)

    def get_plants(self):
        plants = {'plants': []}
        if self.user.plants:
            for plant in self.user.plants:
                water_data_json = vars(plant.water_data)
                plant_json = vars(plant)
                plant_json['water_data'] = water_data_json
                plants['plants'].append(plant_json)

        return plants

    def get_plant_stats(self, plant_id):
        stats_res = []
        plant = self.user.get_plant(plant_id)
        stats = plant.get_stats(self.user.username)

        for stats_doc in stats:
            stats_pair = []
            stats_pair.append(stats_doc['plants']['stats']['timestamp'].isoformat())
            stats_pair.append(stats_doc['plants']['stats']['moisture'])
            stats_res.append(stats_pair)

        return stats_res

    def set_water_now(self, plant_id):
        plant = self.user.get_plant(plant_id)
        plant.set_water_now(self.user.username)

    def get_water_now_data(self):
        water_now_data = {'water_now_data': {}}
        if self.user.plants:
            for plant in self.user.plants:
                water_now_json = {}
                water_now_json[plant.plant_id] = plant.water_now
                water_now_data['water_now_data'].update(water_now_json)

        return water_now_data

    def jsonify_plant(self, plant):
        plant_json = vars(plant)

        return plant_json
