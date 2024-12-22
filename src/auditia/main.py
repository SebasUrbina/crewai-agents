#!/usr/bin/env python
import sys
import warnings

from auditia.crew import Auditia

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

CALL_TRANSCRIPT = """
Agente: Muy buenos días, mi nombre es Carla, ¿en qué puedo ayudarle hoy?
Cliente: Hola, quería consultar sobre el plan de internet hogar. Creo que estoy pagando más de lo que necesito.
Agente: Claro, don Marcelo. Permítame verificar su cuenta. ¿Me puede confirmar su RUT?
Cliente: Sí, es 18.234.567-9.
Agente: Perfecto, gracias. Según veo, actualmente tiene el plan Premium, que incluye 600 Mbps. ¿Es correcto?
Cliente: Sí, pero siento que no utilizo tanto. Mi hija ya no vive con nosotros, y ahora somos solo mi esposa y yo.
Agente: Entiendo. Podemos bajar su plan al Básico de 300 Mbps. Con eso reduciría su cuenta en aproximadamente $10.000 mensuales. ¿Le parece bien?
Cliente: Sí, me parece excelente.
Agente: Listo, ya está actualizado. El cambio se verá reflejado en su próxima boleta. ¿Algo más en que pueda ayudarlo?
Cliente: No, muchas gracias.
Agente: Que tenga un excelente día.
"""

def run():
    """
    Run the crew.
    """
    inputs = {
        "text": CALL_TRANSCRIPT
    }

    Auditia().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "text": CALL_TRANSCRIPT
    }
    try:
        Auditia().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Auditia().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "text": CALL_TRANSCRIPT,
    }
    try:
        Auditia().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
