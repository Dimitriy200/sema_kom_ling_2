#encoding "utf8"
#GRAMMAR_ROOT S


AtrName -> 'музей' | 'зал' | 'собор' | 'филармония' | 'авангард' | 'библиотека' | 'площадь' | 'памятник' | 'церковь' | 'часовня' | 'эшелон' | 'мельница' | 'гора' | 'элеватор' | 'фонтан' | 'курган' | 'опера' | 'планетарий' | 'галерея' | 'погост' | 'арена' | 'Волгоград' | 'сад' | 'парк';

Object -> Noun<gram="inan"> | Noun<gram="anim">;
Adj_AtrName -> (Word<nc-agr[1], gram="sg">) Adj<nc-agr[1]>* AtrName<nc-agr[1], rt> | AtrName<nc-agr[1], rt> Adj<nc-agr[1]> Noun<nc-agr[1]>;

AtrName_Noun -> AtrName<nc-agr[1], rt> Noun<nc-agr[1]> | AtrName<rt> Word<gram="gen"> | AtrName<rt> Noun | Noun<nc-agr[1]> AtrName<nc-agr[1], rt> Adj<nc-agr[1]> Noun<nc-agr[1]>;

Geo_AtrName -> 	Word<nc-agr[1], gram="geo"> AtrName<nc-agr[1], rt> | AtrName<nc-agr[1], rt> Noun<nc-agr[1]> Adj<nc-agr[2], gram="geo"> Noun<nc-agr[2]>;


S -> Adj_AtrName interp(Attraction.Name) | AtrName_Noun interp(Attraction.Name) | Geo_AtrName interp(Attraction.Name) | AtrName interp(Attraction.Name) Object interp(Attraction.Object);
