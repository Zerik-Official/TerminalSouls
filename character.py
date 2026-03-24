"""
character.py
Module that defines the Character class, which represents the characters in the game, both hero and enemy. This class includes attributes for name,
current life, max life, minimum and maximum damage, available potions, as well as methods for generating damage, using special abilities, healing, and taking damage.
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
        Method to generate the character's damage. There is a 10% probability that the attack is a critical hit as long as the character is not in a rage state. If it is,
        the attack will be a guaranteed critical hit. The damage is generated randomly between the character's minimum and maximum damage. If the attack is a critical hit, the damage is doubled.
        
        Args:
            None
        Returns:
            tuple[bool, int]: A tuple indicating whether the attack was a critical hit (True) or not (False), and the damage generated.
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
        Character's special ability. It has a 50% probability of failing. If it fails, it generates no damage. If it succeeds, it generates random damage between 30 and 50.
        If the character is in a rage state, the special ability has a 100% probability of success and cannot be dodged.
        
        Args:
            None
        Returns:
            tuple[bool, int]: A tuple indicating whether the special ability failed (True) or succeeded (False), and the damage generated (0 if failed).
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
        Attempts to heal the character by consuming a potion.

        If the character has at least one potion, it recovers a certain amount of life
        (between 10 and 20) without exceeding max life. Additionally, it reduces the number
        of available potions by one.

        Returns:
            tuple[bool, int]: A tuple indicating whether the healing was successful (True) or not (False), and the amount of life recovered.
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
        Method to receive damage. There is a 10% probability to dodge the attack. If the attack is dodged, no damage is received. If the attacker is in a rage state,
        the attack cannot be dodged. The damage received is subtracted from the character's current life. If current life is less than 0, it is set to 0.

        Args:
            damage (int): The damage to receive
            unavoidable (bool): Indicates whether the attack is unavoidable, in which case it cannot be dodged. Default is False.
        Returns:
            tuple[bool, int]: A tuple indicating whether the attack was dodged (True) or not (False), and the current life after receiving the damage.
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
        Method to verify if the character has died. Returns False if life is greater than 0, otherwise returns True.
        
        Args:
            None
        Returns:
            bool: True if current life is less than or equal to 0, otherwise False.
        """

        return self.current_life <= 0
    
    def apply_rage_buff(self):
        """
        Method to apply the rage state to the character. The next attack will be a critical hit,
        it cannot be dodged, and the special ability will have a 100% success probability and cannot be dodged.

        Args:
            None
        Returns:
            None
        """

        self.next_attack_critical = True
        self.next_attack_unavoidable = True
        self.next_skill_guaranteed = True