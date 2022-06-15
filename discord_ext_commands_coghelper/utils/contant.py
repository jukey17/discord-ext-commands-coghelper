# https://qiita.com/nadu_festival/items/c507542c11fc0ff32529
class ConstantError(Exception):
    """Constantクラスの例外"""

    pass


class ConstantMeta(type):
    """Constantクラスのメタクラス"""

    def __new__(mcs, class_name, bases, dic):
        # 異なるConstantMetaを継承していないか検証する
        sub_classes = [cls for cls in bases if isinstance(cls, ConstantMeta)]
        for sub_cls in sub_classes[1:]:
            if sub_classes[0] != sub_cls:
                raise ConstantError(
                    f"Can't inheritance of [{sub_classes[0].__name__}] and [{sub_cls.__name__}] together"
                )

        # 親クラス同士で定数の衝突が起こっていないか確認
        super_consts = set()
        for base in bases:
            base_consts = ConstantMeta.__get_constant_attr(mcs, base.__dict__)
            collisions = super_consts & base_consts
            if collisions:
                collies_str = ", ".join(collisions)
                raise ConstantError(f"Collision the constant [{collies_str}]")
            super_consts |= base_consts

        # 定義するクラスで定数の再定義をしていないか確認
        new_consts = ConstantMeta.__get_constant_attr(mcs, dic)
        rebinds = super_consts & new_consts
        if rebinds:
            rebinds_str = ", ".join(rebinds)
            raise ConstantError(f"Can't rebind constant [{rebinds_str}]")

        # __init__関数置き換えてインスタンス生成を禁止する
        def _meta__init__(self, *args, **kwargs):
            # インスタンスの生成をしようとした際、ConstantErrorを送出する。
            raise ConstantError("Can't make instance of Constant class")

        # __init__関数を置き換えてインスタンス生成を禁止する。
        dic["__init__"] = _meta__init__

        return type.__new__(mcs, class_name, bases, dic)

    @staticmethod
    def __get_constant_attr(mcs, dic):
        """定数として扱うアトリビュートの集合を取得する"""
        # 特殊なアトリビュートを除くアトリビュートを取得する
        attrs = set(atr for atr in dic if not ConstantMeta.__is_special_func(atr))
        # アトリビュートがすべて定数または例外的にクラス変数に格納可能な
        # 変数であることを確認する
        const_atr = set(atr for atr in attrs if mcs.is_constant_attr(atr))
        var_atr = set(atr for atr in attrs if mcs.is_settable_attr(atr))
        wrong_atr = attrs - (const_atr | var_atr)
        if wrong_atr:
            wrong_atr_str = ", ".join(wrong_atr)
            raise ConstantError(
                f"Attribute [{wrong_atr_str}] were not constant or not settable."
            )
        return const_atr

    @staticmethod
    def __is_special_func(name):
        """特殊アトリビュートかどうかを判定する"""
        return name.startswith("__") and name.endswith("__")

    @classmethod
    def is_constant_attr(mcs, name):
        """定数として扱うアトリビュートか判定する"""
        return not name.startswith("__")

    @classmethod
    def is_settable_attr(mcs, name):
        """例外的にクラス変数に格納することを許可するアトリビュートか判定する"""
        return not mcs.is_constant_attr(name)

    def __setattr__(cls, name, value):
        mcs = type(cls)
        if mcs.is_constant_attr(name) or (not mcs.is_settable_attr(name)):
            raise ConstantError(f"Can't set attribute to Constant [{name}]")
        else:
            super().__setattr__(name, value)


class Constant(metaclass=ConstantMeta):
    """定数クラス"""
