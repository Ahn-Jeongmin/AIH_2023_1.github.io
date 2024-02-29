import excluded as ex
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt

plt.rc("font", family="Malgun Gothic")

urls=['https://www.pressian.com/pages/articles/284148', 'https://www.pressian.com/pages/articles/284170', 'https://www.pressian.com/pages/articles/284142', 'https://www.pressian.com/pages/articles/284125', 'https://www.pressian.com/pages/articles/284123', 'https://www.pressian.com/pages/articles/284089', 'https://www.pressian.com/pages/articles/284060', 'https://www.pressian.com/pages/articles/284020', 'https://www.pressian.com/pages/articles/284016', 'https://www.pressian.com/pages/articles/283992', 'https://www.pressian.com/pages/articles/283959', 'https://www.pressian.com/pages/articles/283951', 'https://www.pressian.com/pages/articles/283946', 'https://www.pressian.com/pages/articles/283910', 'https://www.pressian.com/pages/articles/283834', 'https://www.pressian.com/pages/articles/283823', 'https://www.pressian.com/pages/articles/283820', 'https://www.pressian.com/pages/articles/283806', 'https://www.pressian.com/pages/articles/283800', 'https://www.pressian.com/pages/articles/283792', 'https://www.pressian.com/pages/articles/283762', 'https://www.pressian.com/pages/articles/283747', 'https://www.pressian.com/pages/articles/283724', 'https://www.pressian.com/pages/articles/283712', 'https://www.pressian.com/pages/articles/283672', 'https://www.pressian.com/pages/articles/283658', 'https://www.pressian.com/pages/articles/283626', 'https://www.pressian.com/pages/articles/283641', 'https://www.pressian.com/pages/articles/283624', 'https://www.pressian.com/pages/articles/283606', 'https://www.pressian.com/pages/articles/283602', 'https://www.pressian.com/pages/articles/283590', 'https://www.pressian.com/pages/articles/283555', 'https://www.pressian.com/pages/articles/283552', 'https://www.pressian.com/pages/articles/283514', 'https://www.pressian.com/pages/articles/283496', 'https://www.pressian.com/pages/articles/283497', 'https://www.pressian.com/pages/articles/283475', 'https://www.pressian.com/pages/articles/283481', 'https://www.pressian.com/pages/articles/283459', 'https://www.pressian.com/pages/articles/283418', 'https://www.pressian.com/pages/articles/283412', 'https://www.pressian.com/pages/articles/283389', 'https://www.pressian.com/pages/articles/283397', 'https://www.pressian.com/pages/articles/283380', 'https://www.pressian.com/pages/articles/283363', 'https://www.pressian.com/pages/articles/283352', 'https://www.pressian.com/pages/articles/283350', 'https://www.pressian.com/pages/articles/283348', 'https://www.pressian.com/pages/articles/283340', 'https://www.pressian.com/pages/articles/283338', 'https://www.pressian.com/pages/articles/283331', 'https://www.pressian.com/pages/articles/283319', 'https://www.pressian.com/pages/articles/283236', 'https://www.pressian.com/pages/articles/283171', 'https://www.pressian.com/pages/articles/283168', 'https://www.pressian.com/pages/articles/283152', 'https://www.pressian.com/pages/articles/283101', 'https://www.pressian.com/pages/articles/283120', 'https://www.pressian.com/pages/articles/283112', 'https://www.pressian.com/pages/articles/283103', 'https://www.pressian.com/pages/articles/283082', 'https://www.pressian.com/pages/articles/283075', 'https://www.pressian.com/pages/articles/283056', 'https://www.pressian.com/pages/articles/283045', 'https://www.pressian.com/pages/articles/283028', 'https://www.pressian.com/pages/articles/283030', 'https://www.pressian.com/pages/articles/283031', 'https://www.pressian.com/pages/articles/283013', 'https://www.pressian.com/pages/articles/282952', 'https://www.pressian.com/pages/articles/282933', 'https://www.pressian.com/pages/articles/282892', 'https://www.pressian.com/pages/articles/282851', 'https://www.pressian.com/pages/articles/282837', 'https://www.pressian.com/pages/articles/282641', 'https://www.pressian.com/pages/articles/282816', 'https://www.pressian.com/pages/articles/282780', 'https://www.pressian.com/pages/articles/282722', 'https://www.pressian.com/pages/articles/282659', 'https://www.pressian.com/pages/articles/282656', 'https://www.pressian.com/pages/articles/282654', 'https://www.pressian.com/pages/articles/282644', 'https://www.pressian.com/pages/articles/282557', 'https://www.pressian.com/pages/articles/282618', 'https://www.pressian.com/pages/articles/282606', 'https://www.pressian.com/pages/articles/282565', 'https://www.pressian.com/pages/articles/282554', 'https://www.pressian.com/pages/articles/282515', 'https://www.pressian.com/pages/articles/282486', 'https://www.pressian.com/pages/articles/282484', 'https://www.pressian.com/pages/articles/282444', 'https://www.pressian.com/pages/articles/282460', 'https://www.pressian.com/pages/articles/282453', 'https://www.pressian.com/pages/articles/282229', 'https://www.pressian.com/pages/articles/282430', 'https://www.pressian.com/pages/articles/282404', 'https://www.pressian.com/pages/articles/282390', 'https://www.pressian.com/pages/articles/282383', 'https://www.pressian.com/pages/articles/282350', 'https://www.pressian.com/pages/articles/282339', 'https://www.pressian.com/pages/articles/282323', 'https://www.pressian.com/pages/articles/282293', 'https://www.pressian.com/pages/articles/282317', 'https://www.pressian.com/pages/articles/282268', 'https://www.pressian.com/pages/articles/282256', 'https://www.pressian.com/pages/articles/282237', 'https://www.pressian.com/pages/articles/282232', 'https://www.pressian.com/pages/articles/282214', 'https://www.pressian.com/pages/articles/282211', 'https://www.pressian.com/pages/articles/282194', 'https://www.pressian.com/pages/articles/282195', 'https://www.pressian.com/pages/articles/282178', 'https://www.pressian.com/pages/articles/282029', 'https://www.pressian.com/pages/articles/282164', 'https://www.pressian.com/pages/articles/282144', 'https://www.pressian.com/pages/articles/282125', 'https://www.pressian.com/pages/articles/282052', 'https://www.pressian.com/pages/articles/282047', 'https://www.pressian.com/pages/articles/282044', 'https://www.pressian.com/pages/articles/282019', 'https://www.pressian.com/pages/articles/282031', 'https://www.pressian.com/pages/articles/282011', 'https://www.pressian.com/pages/articles/281985', 'https://www.pressian.com/pages/articles/281991', 'https://www.pressian.com/pages/articles/281924', 'https://www.pressian.com/pages/articles/281922', 'https://www.pressian.com/pages/articles/281911', 'https://www.pressian.com/pages/articles/281899', 'https://www.pressian.com/pages/articles/281891', 'https://www.pressian.com/pages/articles/281882', 'https://www.pressian.com/pages/articles/281874', 'https://www.pressian.com/pages/articles/281847', 'https://www.pressian.com/pages/articles/281834', 'https://www.pressian.com/pages/articles/281829', 'https://www.pressian.com/pages/articles/281821', 'https://www.pressian.com/pages/articles/281812', 'https://www.pressian.com/pages/articles/281807', 'https://www.pressian.com/pages/articles/281787', 'https://www.pressian.com/pages/articles/281729', 'https://www.pressian.com/pages/articles/281764', 'https://www.pressian.com/pages/articles/281715', 'https://www.pressian.com/pages/articles/281684', 'https://www.pressian.com/pages/articles/281702', 'https://www.pressian.com/pages/articles/281694', 'https://www.pressian.com/pages/articles/281693', 'https://www.pressian.com/pages/articles/281627', 'https://www.pressian.com/pages/articles/281620', 'https://www.pressian.com/pages/articles/281613', 'https://www.pressian.com/pages/articles/281611', 'https://www.pressian.com/pages/articles/281607', 'https://www.pressian.com/pages/articles/281597', 'https://www.pressian.com/pages/articles/281518', 'https://www.pressian.com/pages/articles/281506', 'https://www.pressian.com/pages/articles/281488', 'https://www.pressian.com/pages/articles/281492', 'https://www.pressian.com/pages/articles/281493', 'https://www.pressian.com/pages/articles/281484', 'https://www.pressian.com/pages/articles/281461', 'https://www.pressian.com/pages/articles/281341', 'https://www.pressian.com/pages/articles/281438', 'https://www.pressian.com/pages/articles/281420', 'https://www.pressian.com/pages/articles/281365', 'https://www.pressian.com/pages/articles/281301', 'https://www.pressian.com/pages/articles/281312', 'https://www.pressian.com/pages/articles/281303', 'https://www.pressian.com/pages/articles/281292', 'https://www.pressian.com/pages/articles/281295', 'https://www.pressian.com/pages/articles/281282', 'https://www.pressian.com/pages/articles/281280', 'https://www.pressian.com/pages/articles/281251', 'https://www.pressian.com/pages/articles/281217', 'https://www.pressian.com/pages/articles/281203', 'https://www.pressian.com/pages/articles/281202', 'https://www.pressian.com/pages/articles/281164', 'https://www.pressian.com/pages/articles/281113', 'https://www.pressian.com/pages/articles/281108', 'https://www.pressian.com/pages/articles/281102', 'https://www.pressian.com/pages/articles/281073', 'https://www.pressian.com/pages/articles/281057', 'https://www.pressian.com/pages/articles/281047', 'https://www.pressian.com/pages/articles/281042', 'https://www.pressian.com/pages/articles/281054', 'https://www.pressian.com/pages/articles/281018', 'https://www.pressian.com/pages/articles/280997', 'https://www.pressian.com/pages/articles/280973', 'https://www.pressian.com/pages/articles/280938', 'https://www.pressian.com/pages/articles/280825', 'https://www.pressian.com/pages/articles/280817', 'https://www.pressian.com/pages/articles/280808', 'https://www.pressian.com/pages/articles/280797', 'https://www.pressian.com/pages/articles/280799', 'https://www.pressian.com/pages/articles/280743', 'https://www.pressian.com/pages/articles/277923', 'https://www.pressian.com/pages/articles/280715', 'https://www.pressian.com/pages/articles/280710', 'https://www.pressian.com/pages/articles/280691', 'https://www.pressian.com/pages/articles/280690', 'https://www.pressian.com/pages/articles/280688', 'https://www.pressian.com/pages/articles/280592', 'https://www.pressian.com/pages/articles/280587', 'https://www.pressian.com/pages/articles/280624', 'https://www.pressian.com/pages/articles/280579', 'https://www.pressian.com/pages/articles/280494', 'https://www.pressian.com/pages/articles/280455', 'https://www.pressian.com/pages/articles/280426', 'https://www.pressian.com/pages/articles/280406', 'https://www.pressian.com/pages/articles/280383', 'https://www.pressian.com/pages/articles/280386', 'https://www.pressian.com/pages/articles/280376', 'https://www.pressian.com/pages/articles/280355', 'https://www.pressian.com/pages/articles/280311', 'https://www.pressian.com/pages/articles/280321', 'https://www.pressian.com/pages/articles/280287', 'https://www.pressian.com/pages/articles/280281', 'https://www.pressian.com/pages/articles/280259', 'https://www.pressian.com/pages/articles/280254', 'https://www.pressian.com/pages/articles/280238', 'https://www.pressian.com/pages/articles/280222', 'https://www.pressian.com/pages/articles/280221', 'https://www.pressian.com/pages/articles/280218', 'https://www.pressian.com/pages/articles/280203', 'https://www.pressian.com/pages/articles/280010', 'https://www.pressian.com/pages/articles/280164', 'https://www.pressian.com/pages/articles/280151', 'https://www.pressian.com/pages/articles/280125', 'https://www.pressian.com/pages/articles/280088', 'https://www.pressian.com/pages/articles/280068', 'https://www.pressian.com/pages/articles/280057', 'https://www.pressian.com/pages/articles/280025', 'https://www.pressian.com/pages/articles/280009', 'https://www.pressian.com/pages/articles/279977', 'https://www.pressian.com/pages/articles/279946', 'https://www.pressian.com/pages/articles/279911', 'https://www.pressian.com/pages/articles/279884', 'https://www.pressian.com/pages/articles/279872', 'https://www.pressian.com/pages/articles/279838', 'https://www.pressian.com/pages/articles/279828', 'https://www.pressian.com/pages/articles/279837', 'https://www.pressian.com/pages/articles/279789', 'https://www.pressian.com/pages/articles/279776', 'https://www.pressian.com/pages/articles/279778', 'https://www.pressian.com/pages/articles/279754', 'https://www.pressian.com/pages/articles/279735', 'https://www.pressian.com/pages/articles/279750', 'https://www.pressian.com/pages/articles/279740', 'https://www.pressian.com/pages/articles/279732', 'https://www.pressian.com/pages/articles/279713', 'https://www.pressian.com/pages/articles/279661', 'https://www.pressian.com/pages/articles/279660', 'https://www.pressian.com/pages/articles/279535', 'https://www.pressian.com/pages/articles/279532', 'https://www.pressian.com/pages/articles/279520', 'https://www.pressian.com/pages/articles/279512', 'https://www.pressian.com/pages/articles/279457', 'https://www.pressian.com/pages/articles/279446', 'https://www.pressian.com/pages/articles/279445', 'https://www.pressian.com/pages/articles/279429', 'https://www.pressian.com/pages/articles/279426', 'https://www.pressian.com/pages/articles/279428', 'https://www.pressian.com/pages/articles/279423', 'https://www.pressian.com/pages/articles/279411', 'https://www.pressian.com/pages/articles/279261', 'https://www.pressian.com/pages/articles/279378', 'https://www.pressian.com/pages/articles/279361', 'https://www.pressian.com/pages/articles/279312', 'https://www.pressian.com/pages/articles/279315', 'https://www.pressian.com/pages/articles/279297', 'https://www.pressian.com/pages/articles/279267', 'https://www.pressian.com/pages/articles/279272', 'https://www.pressian.com/pages/articles/279256', 'https://www.pressian.com/pages/articles/279235', 'https://www.pressian.com/pages/articles/279234', 'https://www.pressian.com/pages/articles/279233', 'https://www.pressian.com/pages/articles/279200', 'https://www.pressian.com/pages/articles/279098', 'https://www.pressian.com/pages/articles/279080', 'https://www.pressian.com/pages/articles/279072', 'https://www.pressian.com/pages/articles/279082', 'https://www.pressian.com/pages/articles/279077', 'https://www.pressian.com/pages/articles/279038', 'https://www.pressian.com/pages/articles/279061', 'https://www.pressian.com/pages/articles/278983', 'https://www.pressian.com/pages/articles/279002', 'https://www.pressian.com/pages/articles/279016', 'https://www.pressian.com/pages/articles/279010', 'https://www.pressian.com/pages/articles/279007', 'https://www.pressian.com/pages/articles/278995', 'https://www.pressian.com/pages/articles/278865', 'https://www.pressian.com/pages/articles/278897', 'https://www.pressian.com/pages/articles/278887', 'https://www.pressian.com/pages/articles/278881', 'https://www.pressian.com/pages/articles/278855', 'https://www.pressian.com/pages/articles/278849', 'https://www.pressian.com/pages/articles/278848', 'https://www.pressian.com/pages/articles/278804', 'https://www.pressian.com/pages/articles/278790', 'https://www.pressian.com/pages/articles/278792', 'https://www.pressian.com/pages/articles/278794', 'https://www.pressian.com/pages/articles/278779', 'https://www.pressian.com/pages/articles/278783', 'https://www.pressian.com/pages/articles/278708', 'https://www.pressian.com/pages/articles/278715', 'https://www.pressian.com/pages/articles/278696', 'https://www.pressian.com/pages/articles/278695', 'https://www.pressian.com/pages/articles/278685', 'https://www.pressian.com/pages/articles/278630', 'https://www.pressian.com/pages/articles/278636', 'https://www.pressian.com/pages/articles/278621', 'https://www.pressian.com/pages/articles/278583', 'https://www.pressian.com/pages/articles/278560', 'https://www.pressian.com/pages/articles/278552', 'https://www.pressian.com/pages/articles/278558', 'https://www.pressian.com/pages/articles/278549', 'https://www.pressian.com/pages/articles/278548', 'https://www.pressian.com/pages/articles/278515', 'https://www.pressian.com/pages/articles/278491', 'https://www.pressian.com/pages/articles/278478', 'https://www.pressian.com/pages/articles/278476', 'https://www.pressian.com/pages/articles/278474', 'https://www.pressian.com/pages/articles/278471', 'https://www.pressian.com/pages/articles/278371', 'https://www.pressian.com/pages/articles/278366', 'https://www.pressian.com/pages/articles/278339', 'https://www.pressian.com/pages/articles/278321', 'https://www.pressian.com/pages/articles/278317', 'https://www.pressian.com/pages/articles/278030', 'https://www.pressian.com/pages/articles/278283', 'https://www.pressian.com/pages/articles/278296', 'https://www.pressian.com/pages/articles/278287', 'https://www.pressian.com/pages/articles/278269', 'https://www.pressian.com/pages/articles/278273', 'https://www.pressian.com/pages/articles/278253', 'https://www.pressian.com/pages/articles/278256', 'https://www.pressian.com/pages/articles/278241', 'https://www.pressian.com/pages/articles/278171', 'https://www.pressian.com/pages/articles/278214', 'https://www.pressian.com/pages/articles/278193', 'https://www.pressian.com/pages/articles/278187', 'https://www.pressian.com/pages/articles/278174', 'https://www.pressian.com/pages/articles/278168', 'https://www.pressian.com/pages/articles/278162', 'https://www.pressian.com/pages/articles/278131', 'https://www.pressian.com/pages/articles/278133', 'https://www.pressian.com/pages/articles/278084', 'https://www.pressian.com/pages/articles/278079', 'https://www.pressian.com/pages/articles/278047', 'https://www.pressian.com/pages/articles/278069', 'https://www.pressian.com/pages/articles/277965', 'https://www.pressian.com/pages/articles/277942', 'https://www.pressian.com/pages/articles/277650', 'https://www.pressian.com/pages/articles/277932', 'https://www.pressian.com/pages/articles/277878', 'https://www.pressian.com/pages/articles/277854', 'https://www.pressian.com/pages/articles/277744', 'https://www.pressian.com/pages/articles/277788', 'https://www.pressian.com/pages/articles/277782', 'https://www.pressian.com/pages/articles/277765', 'https://www.pressian.com/pages/articles/277755', 'https://www.pressian.com/pages/articles/277737', 'https://www.pressian.com/pages/articles/277696', 'https://www.pressian.com/pages/articles/277693', 'https://www.pressian.com/pages/articles/277663', 'https://www.pressian.com/pages/articles/277665', 'https://www.pressian.com/pages/articles/277669', 'https://www.pressian.com/pages/articles/277629', 'https://www.pressian.com/pages/articles/277604', 'https://www.pressian.com/pages/articles/277590', 'https://www.pressian.com/pages/articles/277583', 'https://www.pressian.com/pages/articles/277542', 'https://www.pressian.com/pages/articles/277549', 'https://www.pressian.com/pages/articles/277498', 'https://www.pressian.com/pages/articles/277483', 'https://www.pressian.com/pages/articles/277479', 'https://www.pressian.com/pages/articles/277465', 'https://www.pressian.com/pages/articles/277449', 'https://www.pressian.com/pages/articles/277442', 'https://www.pressian.com/pages/articles/277434', 'https://www.pressian.com/pages/articles/277422', 'https://www.pressian.com/pages/articles/277414', 'https://www.pressian.com/pages/articles/277403', 'https://www.pressian.com/pages/articles/277378', 'https://www.pressian.com/pages/articles/277370', 'https://www.pressian.com/pages/articles/277315', 'https://www.pressian.com/pages/articles/277322', 'https://www.pressian.com/pages/articles/277300', 'https://www.pressian.com/pages/articles/277284', 'https://www.pressian.com/pages/articles/277268', 'https://www.pressian.com/pages/articles/277242', 'https://www.pressian.com/pages/articles/277204', 'https://www.pressian.com/pages/articles/277217', 'https://www.pressian.com/pages/articles/277156', 'https://www.pressian.com/pages/articles/277166', 'https://www.pressian.com/pages/articles/277186', 'https://www.pressian.com/pages/articles/277104', 'https://www.pressian.com/pages/articles/277084', 'https://www.pressian.com/pages/articles/277059', 'https://www.pressian.com/pages/articles/277056', 'https://www.pressian.com/pages/articles/277037', 'https://www.pressian.com/pages/articles/277032', 'https://www.pressian.com/pages/articles/277034', 'https://www.pressian.com/pages/articles/276897', 'https://www.pressian.com/pages/articles/276943', 'https://www.pressian.com/pages/articles/276930', 'https://www.pressian.com/pages/articles/276928', 'https://www.pressian.com/pages/articles/276902', 'https://www.pressian.com/pages/articles/276898', 'https://www.pressian.com/pages/articles/276890', 'https://www.pressian.com/pages/articles/276882', 'https://www.pressian.com/pages/articles/276806', 'https://www.pressian.com/pages/articles/276856', 'https://www.pressian.com/pages/articles/276781', 'https://www.pressian.com/pages/articles/276822', 'https://www.pressian.com/pages/articles/276767', 'https://www.pressian.com/pages/articles/276725', 'https://www.pressian.com/pages/articles/276711', 'https://www.pressian.com/pages/articles/276571', 'https://www.pressian.com/pages/articles/276688', 'https://www.pressian.com/pages/articles/276681', 'https://www.pressian.com/pages/articles/276674', 'https://www.pressian.com/pages/articles/276660', 'https://www.pressian.com/pages/articles/276567', 'https://www.pressian.com/pages/articles/276579', 'https://www.pressian.com/pages/articles/276564', 'https://www.pressian.com/pages/articles/276557', 'https://www.pressian.com/pages/articles/276543', 'https://www.pressian.com/pages/articles/276483', 'https://www.pressian.com/pages/articles/276472', 'https://www.pressian.com/pages/articles/276464', 'https://www.pressian.com/pages/articles/276452', 'https://www.pressian.com/pages/articles/276421', 'https://www.pressian.com/pages/articles/276400', 'https://www.pressian.com/pages/articles/276388', 'https://www.pressian.com/pages/articles/276385', 'https://www.pressian.com/pages/articles/276379', 'https://www.pressian.com/pages/articles/276268', 'https://www.pressian.com/pages/articles/276262', 'https://www.pressian.com/pages/articles/276255', 'https://www.pressian.com/pages/articles/276239', 'https://www.pressian.com/pages/articles/276236', 'https://www.pressian.com/pages/articles/276225', 'https://www.pressian.com/pages/articles/276212', 'https://www.pressian.com/pages/articles/276156', 'https://www.pressian.com/pages/articles/276174', 'https://www.pressian.com/pages/articles/276165', 'https://www.pressian.com/pages/articles/276145', 'https://www.pressian.com/pages/articles/276143', 'https://www.pressian.com/pages/articles/276095', 'https://www.pressian.com/pages/articles/276044', 'https://www.pressian.com/pages/articles/276049', 'https://www.pressian.com/pages/articles/276053', 'https://www.pressian.com/pages/articles/276041', 'https://www.pressian.com/pages/articles/275993', 'https://www.pressian.com/pages/articles/275987', 'https://www.pressian.com/pages/articles/275978', 'https://www.pressian.com/pages/articles/275973', 'https://www.pressian.com/pages/articles/275005', 'https://www.pressian.com/pages/articles/275868', 'https://www.pressian.com/pages/articles/275852', 'https://www.pressian.com/pages/articles/275859', 'https://www.pressian.com/pages/articles/275840', 'https://www.pressian.com/pages/articles/275820', 'https://www.pressian.com/pages/articles/275802', 'https://www.pressian.com/pages/articles/275801', 'https://www.pressian.com/pages/articles/275793', 'https://www.pressian.com/pages/articles/275783', 'https://www.pressian.com/pages/articles/275772', 'https://www.pressian.com/pages/articles/275744', 'https://www.pressian.com/pages/articles/275742', 'https://www.pressian.com/pages/articles/275712', 'https://www.pressian.com/pages/articles/275705', 'https://www.pressian.com/pages/articles/275702', 'https://www.pressian.com/pages/articles/275694', 'https://www.pressian.com/pages/articles/275678', 'https://www.pressian.com/pages/articles/275600', 'https://www.pressian.com/pages/articles/275464', 'https://www.pressian.com/pages/articles/275556', 'https://www.pressian.com/pages/articles/275554', 'https://www.pressian.com/pages/articles/275555', 'https://www.pressian.com/pages/articles/275552', 'https://www.pressian.com/pages/articles/275547', 'https://www.pressian.com/pages/articles/275541', 'https://www.pressian.com/pages/articles/275530', 'https://www.pressian.com/pages/articles/275534', 'https://www.pressian.com/pages/articles/275507', 'https://www.pressian.com/pages/articles/275497', 'https://www.pressian.com/pages/articles/275485', 'https://www.pressian.com/pages/articles/275484', 'https://www.pressian.com/pages/articles/275400', 'https://www.pressian.com/pages/articles/275385', 'https://www.pressian.com/pages/articles/275413', 'https://www.pressian.com/pages/articles/275429', 'https://www.pressian.com/pages/articles/275391', 'https://www.pressian.com/pages/articles/275390', 'https://www.pressian.com/pages/articles/275374', 'https://www.pressian.com/pages/articles/275372', 'https://www.pressian.com/pages/articles/275368', 'https://www.pressian.com/pages/articles/275335', 'https://www.pressian.com/pages/articles/275334', 'https://www.pressian.com/pages/articles/275317', 'https://www.pressian.com/pages/articles/275301', 'https://www.pressian.com/pages/articles/275249', 'https://www.pressian.com/pages/articles/275250', 'https://www.pressian.com/pages/articles/275244', 'https://www.pressian.com/pages/articles/275239', 'https://www.pressian.com/pages/articles/275235', 'https://www.pressian.com/pages/articles/275234', 'https://www.pressian.com/pages/articles/275219', 'https://www.pressian.com/pages/articles/275213', 'https://www.pressian.com/pages/articles/275199', 'https://www.pressian.com/pages/articles/275189', 'https://www.pressian.com/pages/articles/275161', 'https://www.pressian.com/pages/articles/275149', 'https://www.pressian.com/pages/articles/275144', 'https://www.pressian.com/pages/articles/275114', 'https://www.pressian.com/pages/articles/275092', 'https://www.pressian.com/pages/articles/275105', 'https://www.pressian.com/pages/articles/275096', 'https://www.pressian.com/pages/articles/275045', 'https://www.pressian.com/pages/articles/275036', 'https://www.pressian.com/pages/articles/275040', 'https://www.pressian.com/pages/articles/275027', 'https://www.pressian.com/pages/articles/275028', 'https://www.pressian.com/pages/articles/275008', 'https://www.pressian.com/pages/articles/275024', 'https://www.pressian.com/pages/articles/275009', 'https://www.pressian.com/pages/articles/274925', 'https://www.pressian.com/pages/articles/274972', 'https://www.pressian.com/pages/articles/274973', 'https://www.pressian.com/pages/articles/274950', 'https://www.pressian.com/pages/articles/274938', 'https://www.pressian.com/pages/articles/274889', 'https://www.pressian.com/pages/articles/274913', 'https://www.pressian.com/pages/articles/274900', 'https://www.pressian.com/pages/articles/274865', 'https://www.pressian.com/pages/articles/274786', 'https://www.pressian.com/pages/articles/274768', 'https://www.pressian.com/pages/articles/274730', 'https://www.pressian.com/pages/articles/274736', 'https://www.pressian.com/pages/articles/274733', 'https://www.pressian.com/pages/articles/274725', 'https://www.pressian.com/pages/articles/274727', 'https://www.pressian.com/pages/articles/274724', 'https://www.pressian.com/pages/articles/274702', 'https://www.pressian.com/pages/articles/274707', 'https://www.pressian.com/pages/articles/274689', 'https://www.pressian.com/pages/articles/274684', 'https://www.pressian.com/pages/articles/274667', 'https://www.pressian.com/pages/articles/274657', 'https://www.pressian.com/pages/articles/274650', 'https://www.pressian.com/pages/articles/274644']


#####################
# 전체 단어 빈도를 저장할 Counter 객체
total_word_counts = Counter()

okt = Okt()
for url in urls:
    response = requests.get(url)

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 기사 본문 선택
    article_body_elements = soup.select(
        'div#wrap>div#container>div.inner>div.article_view>div.section.pr10>div.article_body.article_body')
    for article_body_element in article_body_elements:
        # 특수 문자 제거 및 소문자 변환
        article_body = re.sub(r"[^\w\s]", "", str(article_body_element)).lower()

        # 명사 추출
        nouns = okt.nouns(article_body)

        ex.excluded_words.extend(["코로나","코로나바이러스"])

        # 단어 빈도 분석
        word_counts = Counter(word for word in nouns if word not in ex.excluded_words)

        # 단어 빈도를 전체 빈도에 누적
        total_word_counts += word_counts

# 가장 많이 등장한 단어 50개 추출
top_words = total_word_counts.most_common(50)

# 시각화를 위한 데이터 준비
labels, counts = zip(*top_words)
x = np.arange(len(labels))

# 막대 그래프 그리기
plt.bar(x, counts, align="center")
plt.xticks(x, labels)
plt.xlabel("단어")
plt.ylabel("빈도수")
plt.title("프레시안 코로나 <20년 1월-정치> 관련 기사 단어 빈도수 분석")
plt.show()

# 결과 출력
print("프레시안 코로나 관련 <20년 1월-정치> 기사 중 가장 많이 등장한 단어 50개:")
for word, count in top_words:
    print(f"{word}: {count}")

# 사용자 입력 대기
input("Press Enter to exit...")