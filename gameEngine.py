"""
GameEngine.py
This module contains the GameEngine class, which is responsible for handling the main game logic,
including the management of hero and enemy turns, as well as the interaction between both characters.
"""
import random
from character import Character

class GameEngine:
    def __init__(self):
        # Game state
        self.game_active: bool = False
    

    def init_game(self, hero_name: str) -> dict:
        """
        Method to initialize the game. Sets the game state as active, initializes the characters, and returns a startup message with the current data of the hero and enemy.

        Args:
            hero_name (str): The hero's name entered by the user.
        Returns:
            dict: A dictionary containing an initialization message and the current data of the hero and enemy.
        """

        self._init_characters(hero_name)
        self.game_active = True

        return {
            "message": [f"The game has started, get ready {self.hero.name}!"],
            "state": self.show_current_data()
        }
    
    def _init_characters(self, hero_name: str) -> None:
        """
        Internal private method of the engine to initialize the game characters, hero and enemy, with their respective statistics.

        Args:
            hero_name (str): The hero's name entered by the user.
        Returns:
            None
        """

        self.hero: Character = Character(hero_name, 3, 100, 100, 10, 25)
        self.enemy: Character = Character("Thanos", 0, 120, 120, 15, 20)

    def show_current_data(self) -> dict[str, dict[str, str | int]]:
        """
        Method to display the current data of the hero and enemy, including their name, current life, max life, and remaining potions.

        Args:
            None
        Returns:
            dict[str, dict[str, str | int]]: A dictionary with information about both characters.
        """

        return {
            "hero": {
                "name": self.hero.name,
                "current_life": self.hero.current_life,
                "max_life": self.hero.max_life,
                "potions": self.hero.potions,
                    },
            "enemy": {
                "name": self.enemy.name,
                "current_life": self.enemy.current_life,
                "max_life": self.enemy.max_life,
                "potions": self.enemy.potions
            }
        }

    def process_turn(self, option: int) -> dict:
        """
        Method to process the hero's and enemy's turns. Depending on the user's chosen option, the hero's turn is executed first, then the enemy's turn.
        It checks if any character has died and returns a message with the results of both turns along with the current data of the hero and enemy.

        Args:
            option (int): The option chosen by the user for the hero's turn (1 to attack, 2 to use a potion, 3 to use the special ability).
        Returns:
            dict: A dictionary containing a list of messages with the results of both turns and the current data of the hero and enemy.
        """

        messages: list[str] = []

        if not self.game_active:
            return {
                "message": ["The game has not been started or has ended. Please start a new game to continue."],
                "state": self.show_current_data()
            }

        messages.extend(self.hero_turn(option))

        if self.enemy.is_dead():
            self.game_active = False
            messages.append("The hero has defeated the enemy. Good has prevailed!")
            return {
                "message": messages,
                "state": self.show_current_data()
            }
        
        messages.extend(self.enemy_turn())

        if self.hero.is_dead():
            self.game_active = False
            messages.append("The hero has been defeated by the enemy. Game Over!")
            return {
                "message": messages,
                "state": self.show_current_data()
            }
        
        return {
            "message": messages,
            "state": self.show_current_data()
        }
    
    def hero_turn(self, option: int) -> list[str]:
        """
        Method to execute the hero's turn. Depending on the user's chosen option, the hero can attack, use a potion, or use their special ability.

        Args:
            option (int): The option chosen by the user (1 to attack, 2 to use a potion, 3 to use the special ability).
        Returns:
            list[str]: A list of messages describing the actions and results of the hero's turn.
        """

        messages: list[str] = []

        match option:
            case 1:
                critical, damage = self.hero.generate_damage()

                unavoidable: bool = self.hero.next_attack_unavoidable

                dodged, _ = self.enemy.take_damage(damage, unavoidable)

                self.hero.next_attack_unavoidable = False

                fixed_part: str = 'critical hit' if critical else 'normal attack'


                if dodged:
                    messages.append(
                        f"The hero attempted to throw a {fixed_part}, but the enemy managed to dodge it and started mocking the hero."
                        )

                else:
                    if unavoidable:                        
                        messages.append(
                            f"The hero, in a state of rage, connects a powerful critical hit to the enemy, which suffers {damage} critical damage and its life is now at {self.enemy.current_life}. The enemy is in pain from such a blow."
                            )
                    else:
                        messages.append(
                            f"The enemy attempted to dodge a {fixed_part} dealing {damage} damage and failed. The enemy's life is now at {self.enemy.current_life}. The hero celebrates their {fixed_part}."
                            )

                return messages

            case 2:
                result, healed = self.hero.use_cure()

                if result:
                    messages.append(
                        f"Healing was successful: "
                        f"the hero has recovered {healed} life. "
                        f"Current life: {self.hero.current_life}. "
                        f"Remaining potions: {self.hero.potions}"
                    )
                else:
                    messages.append("No potions left. The hero wastes their turn searching their backpack in vain.")
                
                return messages
            
            case 3:
                failure, damage_special_skill = self.hero.special_skill()

                if failure:
                    messages.append(
                        f"The hero failed their special ability and started crying. The enemy lets out a mocking laugh."
                    )
                else:
                    unavoidable: bool = self.hero.next_skill_guaranteed

                    was_dodged, _ = self.enemy.take_damage(damage_special_skill, unavoidable)

                    if was_dodged:
                        self.hero.apply_rage_buff()
                        messages.append(
                            f"The hero made an incredible effort and managed to launch their special ability, but the enemy dodged it and started laughing uncontrollably. "
                            f"The hero enters a state of rage. This guarantees that on their next turn, they will land a critical hit that cannot be dodged, and their next special ability will be cast successfully and cannot be dodged."
                        )
                    else:
                        messages.append(
                            f"The special ability impacts correctly, dealing {damage_special_skill} damage. "
                            f"The enemy is badly hurt and their life is now at {self.enemy.current_life}."
                        )

                    if unavoidable:
                        self.hero.next_skill_guaranteed = False
                    
                return messages
                
    def enemy_turn(self) -> list[str]:
        """
        Method to execute the enemy's turn. The enemy will attempt to heal if their life is less than or equal to 20% of their max life,
        then attack the hero with a hit that can be critical or normal.

        Args:
            None
        Returns:
            list[str]: A list of messages describing the actions and results of the enemy's turn.
        """

        messages: list[str] = []

        life_ratio: float = self.enemy.current_life / self.enemy.max_life

        healed: int = 0

        if life_ratio <= 0.2:
            messages.append("The enemy attempts to channel dark energy to heal themselves...")

            success: bool = random.random() < 0.5

            if success:
                heal_amount: int = random.randint(20, 30)
                life_before: int = self.enemy.current_life
                self.enemy.current_life = min(
                    self.enemy.max_life,
                    self.enemy.current_life + heal_amount
                )
                healed: int = self.enemy.current_life - life_before

                messages.append(
                    f"The enemy manages to heal {healed} life. Current life: {self.enemy.current_life}. The hero starts to worry."
                    )
            else:
                messages.append("The healing fails and the energy dissipates into the air. The hero sighs with relief.")

        critical, damage = self.enemy.generate_damage()

        dodged, _ = self.hero.take_damage(damage)

        fixed_part: str = "critical hit" if critical else "normal attack"

        if dodged:
            messages.append(
                f"The enemy throws a {fixed_part}, but the hero manages to dodge it. The hero sighs, relieved to have dodged the blow in time. "
            )
        else:
            messages.append(
                f"The enemy connects a {fixed_part}, dealing {damage} damage. "
                f"The hero is knocked back quite far and their life is now at {self.hero.current_life}."
            )
        
        return messages