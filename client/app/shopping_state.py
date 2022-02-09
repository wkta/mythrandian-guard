import glvars
from katagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, EventManager, import_pygame
from app.shopping.ShoppingModel import ShoppingModel
from app.shopping.ShoppingView import ShoppingView


pygame = import_pygame()


class ShoppingCtrl(EventReceiver):

    def __init__(self, ref_mod2, ref_vue):
        super().__init__()
        self.ref_mod2 = ref_mod2
        self.ref_vue = ref_vue

    def proc_event(self, ev, source):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)

        # elif ev.type == MyEvTypes.WannaBuySkin:
        #     res = ev.shop.can_buy_item(ev.skin_code)
        #
        #     if ShoppingModel.MCODE_ACHAT_OK == res:
        #         ev.shop.valide_achat_skin(ev.skin_code)
        #         self.ref_vue.signale_achat_ok(ev.skin_code)
        #
        #     elif ShoppingModel.MCODE_ACHAT_TROP_CHER:
        #         self.ref_vue.signale_trop_cher()
        #
        #     elif ShoppingModel.MCODE_ACHAT_PORTRAIT_POSSEDE:
        #         self.ref_vue.signale_portrait_possede()


class ShoppingState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m1 = self.m2 = self.v = self.c = None

    def enter(self):
        self.m2 = ShoppingModel()

        id_portrait_actuel = glvars.the_avatar.portrait_code
        self.v = ShoppingView(self.m2, id_portrait_actuel)
        self.v.turn_on()

        self.c = ShoppingCtrl(self.m2, self.v)
        self.c.turn_on()

    def release(self):
        EventManager.instance().soft_reset()
        self.m1 = self.m2 = self.v = self.c = None
