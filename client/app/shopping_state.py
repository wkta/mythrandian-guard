import os

import glvars
from game_defs import *
from game_events import MyEvTypes
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, EventManager, import_pygame
from pkatagames_sdk.engine import CogObject
from pkatagames_sdk.ext_gui import Trigger, WidgetBo


pygame = import_pygame()


# ------------------------------------------
#  models
# ------------------------------------------
class ShoppingModel(CogObject):

    MCODE_ACHAT_OK, MCODE_ACHAT_TROP_CHER, MCODE_ACHAT_PORTRAIT_POSSEDE = range(1234, 1234 + 3)

    def __init__(self):
        super().__init__()

        # - modern code
        self._portraits_et_prix = {
            AvLooks.OldMan: (100, 0),  # pesos, Mobi
            AvLooks.RiceFarmer: (750, 0),
            AvLooks.Smith: (3000, 0),
            AvLooks.GrandPa: (0, 150),
            AvLooks.Amazon: (0, 300),
            AvLooks.Skeleton: (0, 450),
            AvLooks.GoldenKnight: (0, 750)
        }
        self._list_owned_upgrades = list()
        for owned_skin in self._list_owned_upgrades:
            self._portraits_et_prix[owned_skin] = None

        # - old code
        self.message = 'Pick a new avatar portrait'

    def get_message(self):
        return self.message

    def owns_skin(self, skincode):
        return skincode in self._list_owned_upgrades

    def can_buy_item(self, skin_code):
        if skin_code in self._list_owned_upgrades:
            return self.MCODE_ACHAT_PORTRAIT_POSSEDE

        price_infos = self._portraits_et_prix[skin_code]
        if price_infos[0] != 0:
            if glvars.the_avatar.gold >= price_infos[0]:
                return self.MCODE_ACHAT_OK
        else:
            if glvars.the_avatar.tokenwealth >= price_infos[1]:
                return self.MCODE_ACHAT_OK

        return self.MCODE_ACHAT_TROP_CHER

    def selection_skin(self, skc):
        self.pev(MyEvTypes.PlayerSkinChanges, skin_code=skc)
        if skc not in self._list_owned_upgrades:
            raise ValueError('skin_code={} non possedé'.format(skc))
        # TODO fix
        # glvars.av_identity.set_portrait_code(skc)
        # glvars.av_identity.save_to_server()

    def valide_achat_skin(self, skin_code):
        pass  # TODO fix
        # prix_adhoc = self._portraits_et_prix[skin_code]
        #
        # # - paiement effectif
        # if prix_adhoc[0] != 0:  # dépense pesos
        #     glvars.av_identity.realizeExpense(prix_adhoc[0])
        # else:  # dépense Mobi
        #     solde = glvars.av_identity.get_prem_money()
        #     glvars.av_identity.set_prem_money(solde - prix_adhoc[1])
        #
        # glvars.av_identity.add_upgrade(skin_code)
        # self._portraits_et_prix[skin_code] = None
        # self.selection_skin(skin_code)

    def get_li_prices(self):
        return list(self._portraits_et_prix.values())

    def get_li_items(self):
        return list(self._portraits_et_prix.keys())


# ------------------------------------------
#  view
# ------------------------------------------
class MiniDispPortraits:  # recyclage du DispShop écrit par Paul...

    TRIG_SIZE = (85, 20)
    NB_ITEM_PER_LINE = 7
    POS_INIT = (64, 200)
    POS_RAPPEL_PESOS = (25, 120)
    POS_MESSAGE = (420, 635)
    OFFSET_Y_PORTRAITS = 40
    OFFSET_Y_ITEMS = 10
    DECAL_Y_2E_LIGNE = 100

    def __init__(self, ref_shop_model, id_portrait_actuel):
        self.pos_legende = [32, 128]
        self.pos_legende[1] += self.DECAL_Y_2E_LIGNE

        self._ref_mod = ref_shop_model

        self.li_item_asset = list()
        for skin_code in SUPPORTED_LOOKS:
            WidgetBo.link_resource(
                self._to_gfxid(skin_code), os.sep.join((ASSETS_DIR, ASSOC_IDPORTRAIT_FILENAME[skin_code]))
            )
            self.li_item_asset.append(self._to_gfxid(skin_code))

        # Couleurs
        self.rouge = (255, 8, 8)

        # Fonts
        self.big_font = pygame.font.Font(None, 24)
        self.desc_font = pygame.font.Font(None, 14)

        # --- Gestion du portrait actuel
        self.id_portrait_actuel = id_portrait_actuel

        # --- Items et portraits proposés
        self.li_prix_items = None
        self.li_trigs = self.li_widgs = self.li_labels = None
        self.assoc_trigger_iditem = dict()
        self.generer_offres()  # peuple les 3 listes ci-dessus

        # dico inverse, peut-être utile !
        self.assoc_iditem_trigger = {v: k for k, v in self.assoc_trigger_iditem.items()}

        self.message = self.big_font.render("", True, 'BLACK')
        self.wanna_buy_thing_id = None  # Récupéré par ctrl, pour éviter de déclarer 2 * 7 triggers

        self.label_legende_1er_ligne = self.big_font.render(
            ref_shop_model.get_message(),
            True,
            'BLACK'
        )

    @classmethod
    def _to_gfxid(cls, skin_code):
        return 'skin_portrait{}x2'.format(skin_code)

    def informe_achat_item(self, skin_code):
        skin_name = AvLooks.inv_map[skin_code]
        txt = "Achat du skin {} >> OK".format(skin_name)
        self.message = self.big_font.render(txt, True, 'BLACK')
        self.wanna_buy_thing_id = None

        self.generer_offres()
        # trig_a_changer = self.assoc_iditem_trigger[skin_code]
        # trig_a_changer.setLabel('Activate')

    def feedback_achat_portrait(self):
        txt = "Achat du portrait OK"
        self.message = self.big_font.render(txt, True, 'BLACK')
        self.wanna_buy_thing_id = None

    def feedback_trop_cher(self):
        txt = "Pas assez de ressources! ($ ou MOBI)"
        self.message = self.big_font.render(txt, True, self.rouge)

    def feedback_inventaire_plein(self):
        txt = "L'inventaire est plein"
        self.message = self.big_font.render(txt, True, self.rouge)

    def feedback_portrait_possede(self):
        txt = "Vous possédez déjà ce portrait"
        self.message = self.big_font.render(txt, True, self.rouge)

    @staticmethod
    def _formatte_cout(cout_infos):
        assert cout_infos is not None
        if cout_infos[0] != 0:
            return '{} $'.format(cout_infos[0])
        return '{} Mobi'.format(cout_infos[1])

    # méthodes métier
    def generer_offres(self):
        """
        Génère les widgets, labels, et triggers de l'affichage
        Normalement appelée uniquement dans le constructeur
        :return:
        """
        self.li_prix_items = self._ref_mod.get_li_prices()

        self.li_widgs = list()
        self.li_trigs = list()
        self.assoc_trigger_iditem = dict()
        self.li_labels = list()

        #offset_y = self.OFFSET_Y_PORTRAITS
        offset_y = -128
        cpt = 0
        for iditem in SUPPORTED_LOOKS:
            x, y = self.pos_case_vers_pos_ecran(cpt)
            img = WidgetBo(self.li_item_asset[cpt], (x, y))
            cout = self.li_prix_items[cpt]
            if cout is not None:
                texte_adhoc = MiniDispPortraits._formatte_cout(cout)
            else:
                texte_adhoc = 'owned skin'

            lbl = self.desc_font.render(texte_adhoc, True, 'DARKRED')
            buy_trig = Trigger((x, y + 110 + offset_y), self.TRIG_SIZE)

            if self._ref_mod.owns_skin(iditem):
                buy_trig.setLabel('Activate')
            else:
                buy_trig.setLabel('Buy')

            self.li_widgs.append(img)
            self.li_labels.append((lbl, (x + 25, y + 90 + offset_y)))
            self.li_trigs.append(buy_trig)
            self.assoc_trigger_iditem[buy_trig] = iditem
            cpt += 1

    def pos_case_vers_pos_ecran(self, num_case):
        """
        :param num_case: Numéro de la case dans la liste d'items à acheter dans le shop
        :return: Un couple x,y indiquant la position du coin supérieur gauche de l'image de l'item/portrait sur la map
        """
        linerank = num_case % self.NB_ITEM_PER_LINE
        x, y = self.POS_INIT
        y += self.DECAL_Y_2E_LIGNE
        x += 100 * linerank
        return x, y

    def quel_trigger_touche(self, clickpos):
        for trigger_obj, iditem in self.assoc_trigger_iditem.items():
            if trigger_obj.contains(clickpos):
                self.wanna_buy_thing_id = iditem
                return trigger_obj.getLabel()  # signale que c'est BON

    def get_wanna_buy_thing_id(self):
        return self.wanna_buy_thing_id

    def do_paint(self, screen):
        for widg in self.li_widgs:
            widg.draw(screen)

        for lbl in self.li_labels:
            text, pos = lbl
            screen.blit(text, pos)

        for trig in self.li_trigs:
            trig.draw(screen, 'DARKRED')

        screen.blit(self.label_legende_1er_ligne, self.pos_legende)
        screen.blit(self.message, self.POS_MESSAGE)


class ShoppingView(EventReceiver):

    def __init__(self, ref_mod2, id_portrait_actuel):
        super().__init__()

        self.ref_mod2 = ref_mod2
        self.disp2 = MiniDispPortraits(self.ref_mod2, id_portrait_actuel)

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            scr = ev.screen

            scr.fill('antiquewhite3')
            self.disp2.do_paint(scr)
            return

        # if ev.type == PlayerBuysPortrait
        # - cest géré par la vignette déjà...

        if ev.type == pygame.MOUSEBUTTONDOWN:
            # - gérer les achats
            tmp = self.disp2.quel_trigger_touche(ev.pos)
            if tmp is not None:
                someid = self.disp2.get_wanna_buy_thing_id()
                if tmp == 'Buy':
                    self.pev(MyEvTypes.WannaBuySkin, skin_code=someid, shop=self.ref_mod2)
                else:
                    self.pev(MyEvTypes.EquipOwnedSkin, skin_code=someid)

    def signale_achat_ok(self, skin_code):
        self.disp2.informe_achat_item(skin_code)

    def signale_trop_cher(self):
        self.disp2.feedback_trop_cher()

    def signale_portrait_possede(self):
        self.disp2.feedback_portrait_possede()


# ------------------------------------------
#  ctrl
# ------------------------------------------
class ShoppingCtrl(EventReceiver):

    def __init__(self, ref_mod2, ref_vue):
        super().__init__()
        self.ref_mod2 = ref_mod2
        self.ref_vue = ref_vue

    def proc_event(self, ev, source):
        if ev.type == pygame.QUIT:
            self.pev(EngineEvTypes.POPSTATE)
            return

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == MyEvTypes.EquipOwnedSkin:
            if self.ref_mod2.owns_skin(ev.skin_code):
                self.ref_mod2.selection_skin(ev.skin_code)

        elif ev.type == MyEvTypes.WannaBuySkin:
            res = ev.shop.can_buy_item(ev.skin_code)  # contrôle si achat possible!

            if ShoppingModel.MCODE_ACHAT_OK == res:
                ev.shop.valide_achat_skin(ev.skin_code)
                self.ref_vue.signale_achat_ok(ev.skin_code)

            elif ShoppingModel.MCODE_ACHAT_TROP_CHER:
                self.ref_vue.signale_trop_cher()

            elif ShoppingModel.MCODE_ACHAT_PORTRAIT_POSSEDE:
                self.ref_vue.signale_portrait_possede()


class ShoppingState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m1 = self.m2 = self.v = self.c = None

    def enter(self):
        print('## ----------- entree ds ShopState')
        self.m2 = ShoppingModel()  # portraits de mec

        id_portrait_actuel = glvars.the_avatar.portrait_code
        self.v = ShoppingView(self.m2, id_portrait_actuel)
        self.v.turn_on()

        # self.barre_spe = TradeRelatedNavbar()
        # self.barre_spe.turn_on()

        # self.cashbar = CashbarV(glvars.av_identity)
        # self.cashbar.turn_on()

        self.c = ShoppingCtrl(self.m2, self.v)
        self.c.turn_on()

        # if glvars.vignette is None:
        #     glvars.vignette = AvatarStatusBarView(glvars.av_identity, False)
        # glvars.vignette.turn_on()

    def release(self):
        # Persistance de l'avatar
        # glvars.av_identity.save_to_server()
        EventManager.instance().soft_reset()
        self.m1 = self.m2 = self.v = self.c = None
