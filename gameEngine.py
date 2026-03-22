"""
GameEngine.py
Este módulo contiene la clase GameEngine, que es responsable de manejar la lógica principal del juego,
incluyendo la gestión de los turnos del héroe y el enemigo, así como la interacción entre ambos personajes.
"""
import random
from character import Character

class GameEngine:
    def __init__(self):
        # Character initialization
        self.hero: Character = Character("", 3, 100, 100, 10, 25)
        self.enemy: Character = Character("Thanos", 0, 120, 120, 15, 20)

        # Game state
        self.game_active: bool = False
    

    def init_game(self, hero_name: str) -> dict:
        """
        Metodo para iniciar el juego, establece el estado del juego como activo y devuelve un mensaje de inicio junto con los datos actuales del héroe y el enemigo.

        Args:
            hero_name (str): El nombre del héroe ingresado por el usuario.
        Returns:
            dict: Un diccionario que contiene un mensaje de inicio y los datos actuales del héroe y el enemigo.
        """
        self.hero.name = hero_name
        self.game_active = True

        return {
            "message": [f"¡El juego ha comenzado, preparate {self.hero.name}!"],
            "state": self.show_current_data()
        }
    
    def process_turn(self, option: int) -> dict:
        """
        Metodo para procesar el turno del héroe y el enemigo, dependiendo de la opción elegida por el usuario, se ejecuta el turno del héroe y luego el turno del enemigo, 
        se verifica si alguno de los personajes ha muerto y se devuelve un mensaje con los resultados de ambos turnos junto con los datos actuales del héroe y el enemigo.

        Args:
            option (int): La opción elegida por el usuario para el turno del héroe (1 para atacar, 2 para usar una poción, 3 para usar la habilidad especial).
        Returns:
            dict: Un diccionario que contiene una lista de mensajes con los resultados de ambos turnos y los datos actuales del héroe y el enemigo.
        """
        messages: list[str] = []

        if not self.game_active:
            return {
                "message": ["El juego no ha sido iniciado o ha finalizado. Por favor, inicia un nuevo juego para continuar."],
                "state": self.show_current_data()
            }

        messages.extend(self.hero_turn(option))

        if self.enemy.is_dead():
            self.game_active = False
            messages.append("El héroe ha logrado derrotar al enemigo. ¡El bien ha ganado!")
            return {
                "message": messages,
                "state": self.show_current_data()
            }
        
        messages.extend(self.enemy_turn())

        if self.hero.is_dead():
            self.game_active = False
            messages.append("El héroe ha sido derrotado por el enemigo. ¡Game Over!")
            return {
                "message": messages,
                "state": self.show_current_data()
            }
        
        return {
            "message": messages,
            "state": self.show_current_data()
        }
    
    def show_current_data(self) -> dict[str, dict[str, str | int]]:
        """
        Metodo para mostrar los datos actuales del héroe y el enemigo, incluyendo su nombre, vida actual, vida máxima y pociones restantes.

        Args:
            None
        Returns:
            dict[str, dict[str, str | int]]: Un diccionario con la información de ambos personajes.
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

    def hero_turn(self, option: int) -> list[str]:
        """
        Metodo para ejecutar el turno del héroe, dependiendo de la opción elegida por el usuario, el héroe puede atacar, usar una poción o usar su habilidad especial.

        Args:
            option (int): La opción elegida por el usuario (1 para atacar, 2 para usar una poción, 3 para usar la habilidad especial).
        Returns:
            list[str]: Una lista de mensajes que describen las acciones y resultados del turno del héroe.
        """

        messages: list[str] = []

        match option:
            case 1:
                critical, damage = self.hero.generate_damage()

                unavoidable: bool = self.hero.next_attack_unavoidable

                dodged, _ = self.enemy.take_damage(damage, unavoidable)

                self.hero.next_attack_unavoidable = False

                fixed_part: str = 'golpe critico' if critical else 'golpe normal'


                if dodged:
                    messages.append(
                        f"El héroe ha intentado lanzar un {fixed_part}, pero, el enemigo ha logrado esquivarlo y ha empezado a burlarse del héroe."
                        )

                else:
                    if unavoidable:                        
                        messages.append(
                            f"El héroe en un estado de furía, conecta un potente golpe critico al enemigo, el cual sufre {damage} de daño critico y su vida queda en {self.enemy.current_life}, este queda adolorido por tal golpe."
                            )
                    else:
                        messages.append(
                            f"El enemigo ha intentado esquivar un {fixed_part}, de {damage} de daño y ha fallado, la vida del enemigo quedó en {self.enemy.current_life}, el héroe festeja su {fixed_part}."
                            )

                return messages

            case 2:
                result, healed = self.hero.use_cure()

                if result:
                    messages.append(
                        f"La curación fue exitosa: "
                        f"el héroe ha recuperado {healed} de vida. "
                        f"Vida actual: {self.hero.current_life}. "
                        f"Pociones restantes: {self.hero.potions}"
                    )
                else:
                    messages.append("Sin pociones restantes, el héroe pierde el turno mientras rebusca inútilmente en su mochila.")
                
                return messages
            
            case 3:
                failure, damage_special_skill = self.hero.special_skill()

                if failure:
                    messages.append(
                        f"El héroe ha fallado su hábilidad especial y ha empezado a llorar, el enemigo suelta una risa burlona"
                    )
                else:
                    unavoidable: bool = self.hero.next_skill_guaranteed

                    was_dodged, _ = self.enemy.take_damage(damage_special_skill, unavoidable)

                    if was_dodged:
                        self.hero.apply_rage_buff()
                        messages.append(
                            f"El héroe ha hecho un esfuerzo increible y ha logrado lanzar su habilidad especial, pero, el enemigo ha logrado esquivarla y este empieza a reirse descontroladamente. "
                            f"El héroe entra en estado de furia, esto garantiza que en su próximo turno, logre asestar un golpe critico, no puedan esquivar su ataque y además, garantiza que su próxima habilidad especial, sea casteada exitosamente y no sea esquivada."
                        )
                    else:
                        messages.append(
                            f"La habilidad especial impacta correctamente causando {damage_special_skill} de daño. "
                            f"El enemigo queda bastante herido y su vida quedó en {self.enemy.current_life}."
                        )

                    if unavoidable:
                        self.hero.next_skill_guaranteed = False
                    
                return messages
                

    def enemy_turn(self) -> list[str]:
        """
        Metodo para ejecutar el turno del enemigo.

        Args:
            None
        Returns:
            list[str]: Una lista de mensajes que describen las acciones y resultados del turno del enemigo.
        """

        messages: list[str] = []

        life_ratio: float = self.enemy.current_life / self.enemy.max_life

        healed: int = 0

        if life_ratio <= 0.2:
            messages.append("El enemigo intenta canalizar energía oscura para curarse...")

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
                    f"El enemigo logra curarse {healed} de vida. Vida actual: {self.enemy.current_life}. El héroe empieza a preocuparse"
                    )
            else:
                messages.append("La curación falla y la energía se disipa en el aire... El héroe suspira aliviado.")

        critical, damage = self.enemy.generate_damage()

        dodged, _ = self.hero.take_damage(damage)

        fixed_part: str = "golpe crítico" if critical else "golpe normal"

        if dodged:
            messages.append(
                f"El enemigo lanza un {fixed_part}, pero el héroe logra esquivarlo este suelta un suspiro por haber logrado esquivar el golpe a tiempo. "
            )
        else:
            messages.append(
                f"El enemigo conecta un {fixed_part} causando {damage} de daño. "
                f"El héroe sale disparado bastante lejos y su vida quedó en {self.hero.current_life}."
            )
        
        return messages