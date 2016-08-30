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

        for stats_dict in stats:
            now = datetime.datetime.now()
            day_ago = now - datetime.timedelta(1)
            if stats_dict['timestamp'] >= day_ago and stats_dict['timestamp'] <= now:
                time_of_day = []
                stats_pair = []
                time_of_day.append(stats_dict['timestamp'].hour)
                time_of_day.append(stats_dict['timestamp'].minute)
                time_of_day.append(stats_dict['timestamp'].second)
                stats_pair.append(time_of_day)
                stats_pair.append(stats_dict['moisture'])
                stats_res.append(stats_pair)

        return stats_res

    def jsonify_plant(self, plant):
        plant_json = vars(plant)

        return plant_json
