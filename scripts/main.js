import {
  EDGEHEART_COMPETENCIES,
  auditEdgeheartCompetencies,
  registerEdgeheartCompetencies
} from "./competencies.js";

Hooks.once("init", () => {
  const module = game.modules.get("edgeheart");
  if (module) {
    module.api = {
      competencies: EDGEHEART_COMPETENCIES,
      auditCompetencies: auditEdgeheartCompetencies,
      registerCompetencies: registerEdgeheartCompetencies
    };
  }

  console.log("Edgeheart | init");
});

Hooks.once("ready", async () => {
  try {
    const result = await registerEdgeheartCompetencies();
    console.log(`Edgeheart | ready; Competency registration status: ${result.status}`);
  } catch (error) {
    console.error("Edgeheart | Competency registration failed.", error);
    if (game.user?.isGM) {
      ui.notifications?.error(
        "Edgeheart could not initialize its Daggerheart Competencies. See the console for details."
      );
    }
  }
});
