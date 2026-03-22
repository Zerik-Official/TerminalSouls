from character_manager import Character
from utils import generic_input
import random

class GameEngine:
    def __init__(self):
        self.hero: Character = Character("Iro-Man", 3, 100, 100, 10, 25)
        self.enemy: Character = Character("Thanos", 0, 120, 120, 15, 20)
        self.game_active: bool = False
    

    def init_game(self):
        """Metodo para iniciar el juego"""
        self.game_active = True

        while self.game_active:
            self.hero_turn()

            if self.enemy.is_dead():
                print(f"{self.enemy.name} ha sido derrotado")
                self.game_active = False
                break

            self.enemy_turn()

            if self.hero.is_dead():
                print(f"{self.hero.name} ha sido derrotado")
                self.game_active = False
                break
    
    def show_option(self):
        print(f"Game stats: Hero life: {self.hero.current_life} / {self.hero.max_life} Potions: {self.hero.potions} | Enemy life: {self.enemy.current_life} / {self.enemy.max_life}")
        print(
        "\n1. Atacar"
        "\n2. Curar"
        "\n3. Usar la habilidad especial")

    def hero_turn(self):
        self.show_option()
        option: int = generic_input("Por favor, introduce tu acción: ", int)

        match option:
            case 1:
                critical, damage = self.hero.generate_damage()

                unavoidable: bool = self.hero.next_attack_unavoidable

                dodged, _ = self.enemy.take_damage(damage, unavoidable)

                self.hero.next_attack_unavoidable = False

                fixed_part: str = 'golpe critico' if critical else 'golpe normal'

                if dodged:
                    print(
                        f"El héroe ha intentado lanzar un {fixed_part}, pero, el enemigo ha logrado esquivarlo y ha empezado a burlarse del héroe."
                    )
                else:
                    if unavoidable:
                        print(f"El héroe en un estado de furía, conecta un potente golpe critico al enemigo, el cual sufre {damage} de daño critico y su vida queda en {self.enemy.current_life}, este queda adolorido por tal golpe.")
                    else:
                        print(f"El enemigo ha intentado esquivar un {fixed_part}, de {damage} de daño y ha fallado, la vida del enemigo quedó en {self.enemy.current_life}, el héroe festeja su {fixed_part}.")

            case 2:
                result, healed = self.hero.use_cure()

                if result:
                    print(
                        f"La curación fue exitosa: "
                        f"el héroe ha recuperado {healed} de vida. "
                        f"Vida actual: {self.hero.current_life}. "
                        f"Pociones restantes: {self.hero.potions}"
                    )
                else:
                    print("Sin pociones restantes, el héroe pierde el turno mientras rebusca inútilmente en su mochila.")
            
            case 3:
                failure, damage_special_skill = self.hero.special_skill()

                if failure:
                    print(
                        f"El héroe ha fallado su hábilidad especial y ha empezado a llorar, el enemigo suelta una risa burlona"
                    )
                else:
                    unavoidable: bool = self.hero.next_skill_guaranteed

                    was_dodged, _ = self.enemy.take_damage(damage_special_skill, unavoidable)

                    if was_dodged:
                        self.hero.apply_rage_buff()
                        print(
                            f"El héroe ha hecho un esfuerzo increible y ha logrado lanzar su habilidad especial, pero, el enemigo ha logrado esquivarla y este empieza a reirse descontroladamente. "
                            f"El héroe entra en estado de furia, esto garantiza que en su próximo turno, logre asestar un golpe critico, no puedan esquivar su ataque y además, garantiza que su próxima habilidad especial, sea casteada exitosamente y no sea esquivada."
                        )
                    else:
                        print(
                            f"La habilidad especial impacta correctamente causando {damage_special_skill} de daño. "
                            f"El enemigo queda bastante herido y su vida quedó en {self.enemy.current_life}."
                        )

                    if unavoidable:
                        self.hero.next_skill_guaranteed = False
                

    def enemy_turn(self):
        print(f"\n--- Turno de {self.enemy.name} ---")

        life_ratio: float = self.enemy.current_life / self.enemy.max_life

        healed: int = 0
        did_heal: bool = False

        if life_ratio <= 0.2:
            print("El enemigo intenta canalizar energía oscura para curarse...")

            success: bool = random.random() < 0.5

            if success:
                heal_amount = random.randint(20, 30)
                life_before = self.enemy.current_life
                self.enemy.current_life = min(
                    self.enemy.max_life,
                    self.enemy.current_life + heal_amount
                )
                healed = self.enemy.current_life - life_before
                did_heal = True

                print(f"El enemigo logra curarse {healed} de vida. Vida actual: {self.enemy.current_life}. El héroe empieza a preocuparse")
            else:
                print("La curación falla y la energía se disipa en el aire... El héroe suspira aliviado.")

        critical, damage = self.enemy.generate_damage()

        dodged, _ = self.hero.take_damage(damage)

        fixed_part: str = "golpe crítico" if critical else "golpe normal"

        if dodged:
            print(
                f"El enemigo lanza un {fixed_part}, pero el héroe logra esquivarlo este suelta un suspiro por haber logrado esquivar el golpe a tiempo. "
            )
        else:
            print(
                f"El enemigo conecta un {fixed_part} causando {damage} de daño. "
                f"La vida del héroe queda en {self.hero.current_life}."
            )


game = GameEngine()
print("el juego va a iniciar")
game.init_game()