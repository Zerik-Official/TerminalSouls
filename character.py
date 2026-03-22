"""
character.py
Modulo que define la clase Character, la cual representa a los personajes del juego, tanto el héroe como el enemigo. Esta clase incluye atributos para el nombre, 
vida actual, vida máxima, daño mínimo y máximo, pociones disponibles, así como métodos para generar daño, usar habilidades especiales, curarse y recibir daño.
"""
import random

class Character:
    def __init__(self, name: str, potions: int, current_life: int, max_life: int, min_damage: int, max_damage: int):

        # Character stats
        self.name: str = name
        self.potions: int = potions
        self.current_life: int = current_life
        self.max_life: int = max_life
        self.min_damage: int = min_damage
        self.max_damage: int = max_damage

        # Character rage states
        self.next_attack_critical: bool = False
        self.next_attack_unavoidable: bool = False
        self.next_skill_guaranteed: bool = False
    
    def generate_damage(self) -> tuple[bool, int]:
        """
        Metodo para generar el daño del personaje, hay una probabilidad del 10% de que el ataque sea un golpe critico siempre y cuando, el no esté en estado de furia, si lo está,
        el ataque será un golpe critico garantizado, el daño se genera aleatoriamente entre el daño mínimo y máximo del personaje, si el ataque es un golpe critico, el daño se duplica.
        
        Args:
            None
        Returns:
            tuple[bool, int]: Una tupla que indica si el ataque fue un golpe critico (True) o no (False), y el daño generado.
        """

        damage: int = random.randint(self.min_damage, self.max_damage)

        if self.next_attack_critical:
            self.next_attack_critical = False
            return True, damage * 2

        probability_of_critical: bool = random.random() <= 0.10

        if probability_of_critical:
            return True, damage * 2
        return False, damage

    def special_skill(self) -> tuple[bool, int]:
        """
        Habilidad especial del personaje, tiene una probabilidad del 50% de fallar, si falla no genera daño, si tiene éxito genera un daño aleatorio entre 30 y 50, 
        si el personaje está en estado de furia, la habilidad especial tiene un 100% de probabilidad de éxito y no puede ser esquivada.
        
        Args:
            None
        Returns:
            tuple[bool, int]: Una tupla que indica si la habilidad especial falló (True) o tuvo éxito (False), y el daño generado (0 si falló).
        """
        damage_special_skill: int = random.randint(30, 50)
        if self.next_skill_guaranteed:
            return False, damage_special_skill
        
        failure: bool = random.random() < 0.5

        if failure:
            return True, 0
        
        return False, damage_special_skill
    
    def use_cure(self) -> tuple[bool, int]:
        """
        Intenta curar al personaje consumiendo una poción.

        Si el personaje tiene al menos una poción, recupera una cantidad de vida
        (entre 10 y 20) sin superar la vida máxima. Además, reduce en uno el número
        de pociones disponibles.

        Returns:
            tuple[bool, int]: Una tupla que indica si la curación fue exitosa (True) o no (False), y la cantidad de vida recuperada.
        """
        if self.potions <= 0:
            return False, 0

        cured_quantity: int = random.randint(10, 20)

        life_before: int = self.current_life
        new_life: int = self.current_life + cured_quantity
        self.current_life = min(self.max_life, new_life)

        real_healed: int = self.current_life - life_before

        self.potions -= 1

        return True, real_healed

    def take_damage(self, damage: int, unavoidable: bool = False) -> tuple[bool, int]:
        """
        Metodo para recibir daño, hay una probabilidad del 10% de esquivar el ataque, si el ataque es esquivado, no se recibe daño, si el atacante tiene el estado de furia, 
        el ataque no puede ser esquivado, el daño recibido se resta de la vida actual del personaje, si la vida actual es menor a 0, se establece en 0.

        Args:
            damage (int): El daño a recibir
            unavoidable (bool): Indica si el ataque es inevitable, en cuyo caso no se puede esquivar. Por defecto es False.
        Returns:
            tuple[bool, int]: Una tupla que indica si el ataque fue esquivado (True) o no (False), y la vida actual después de recibir el daño.
        """
        if unavoidable:
            self.current_life = max(self.current_life - damage, 0)

            return False, self.current_life
        
        dodging_probability: bool = random.random() <= 0.10

        if dodging_probability:
            return True, self.current_life

        self.current_life = max(self.current_life - damage, 0)
        return False, self.current_life
    
    def is_dead(self) -> bool:
        """
        Metodo para verificar si el personaje ha muerto, devuelve False si la vida es mayor a 0, caso contrario devuelve True
        
        Args:
            None
        Returns:
            bool: True si la vida actual es menor o igual a 0, de lo contrario False.
        """
        return self.current_life <= 0
    
    def apply_rage_buff(self):
        """
        Metodo para aplicar el estado de furia al personaje, el siguiente ataque del personaje será un golpe critico, 
        no podrá ser esquivado, su habilidad especial tendrá un 100% de probabilidad de éxito además no podrá ser esquivada.

        Args:
            None
        Returns:
            None
        """
        self.next_attack_critical = True
        self.next_attack_unavoidable = True
        self.next_skill_guaranteed = True