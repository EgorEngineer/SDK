import prioritizationMethods as pm

# Пример работы с RICE
rice = pm.RICE(reach=5000, impact=4, confidence=80, effort=30)
print("RICE Score:", rice.calculate_rice_score())

# Пример работы с ICE
ice = pm.ICE(impact=8, confidence=90, effort=20)
print("ICE Score:", ice.calculate_ice_score())

# Пример работы с Kano
kano = pm.Kano()
kano.add_feature("Feature 1", customer_satisfaction=1, functionality=1)
kano.add_feature("Feature 2", customer_satisfaction=1, functionality=0)
print("One-dimensional Features:", kano.get_features_by_category('One-dimensional'))
print("Attractive Features:", kano.get_features_by_category('Attractive'))

