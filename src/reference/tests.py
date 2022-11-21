from django.test import TestCase

# Create your tests here.
from reference.models import Author, Serie, Genre, Publisher

# Author filling
b = Author(name='Agatha', surname='Christie')
b.save()
b = Author(name='Isaac', surname='Asimov')
b.save()
b = Author(name='Artur Conan', surname='Doyle')
b.save()
b = Author(name='Владислав', surname='Крапивин')
b.save()
b = Author(name='Эдит', surname='Блайтон')
b.save()

# Serie filling
b = Serie(name='Пять юных сыщиков и верный пес',
          description='Пятеро Тайноискателей – Фатти, Пип, Бетси, Ларри и Дейзи и их верный '
                      'друг и помощник скотч-терьер Бастер живут в английском городке Питерсвуде, '
                      'недалеко от Лондона. Их штаб-квартира – летний домик в саду Фатти. '
                      'Здесь Тайноискатели хранят парики, накладные бороды и усы, одежды '
                      'нищего, старьевщика, цыганки, трубочиста. Этот гардероб Тайноискатели '
                      'используют во время расследований многих загадочных происшествий. '
                      'Но ребятам все время мешает местный полицейский Гун…')
b.save()
b = Serie(name='Великолепная пятерка',
          description='Четверо друзей и пес противостоят контрабандистам, фальшивомонетчикам, '
                      'грабителям и другим преступникам')
b.save()
b = Serie(name='Шерлок Холмс')
b.save()
b = Serie(name='Эркюль Пуаро')
b.save()

# Genre filling
b = Genre(name='Детективы', description='Классический, шпионский, исторический.')
b.save()
b = Genre(name='Документальная Литература', description='Биография, мемуары, география.')
b.save()
b = Genre(name='Дом и семья', description='Кулинария, хобби, развечения.')
b.save()
b = Genre(name='Исскуство', description='Музыка, кино, театр.')
b.save()
b = Genre(name='Литература для детей', description='Сказки, игры, детская остросюжетная литература.')
b.save()
b = Genre(name='Проза', description='Роман, повесть, классическая проза, историческая проза.')
b.save()
b = Genre(name='Приключения', description='Вестерн, историчекие приключения, рыцарский роман.')
b.save()
b = Genre(name='Фантастика', description='Фентези, фантастика, альтернативная история.')
b.save()

# Publisher filling
b = Publisher(name='ACT')
b.save()
b = Publisher(name='Pinguin Publishing')
b.save()
b = Publisher(name='Harper Collins')
b.save()
b = Publisher(name='Эксмо')
b.save()


