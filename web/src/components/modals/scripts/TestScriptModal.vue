<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="min-width: 50vw">
      <q-bar>
        Script Test
        <q-space />
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip class="bg-white text-primary">Close</q-tooltip>
        </q-btn>
      </q-bar>
      <q-form @submit.prevent="runTestScript">
        <q-card-section>
          <tactical-dropdown
            :rules="[val => !!val || '*Required']"
            label="Select Agent to run script on"
            v-model="agent"
            :options="agentOptions"
            mapOptions
            outlined
          />
        </q-card-section>
        <q-card-section>
          <q-select
            label="Script Arguments (press Enter after typing each argument)"
            filled
            v-model="args"
            use-input
            use-chips
            multiple
            hide-dropdown-icon
            input-debounce="0"
            new-value-mode="add"
            dense
          />
        </q-card-section>
        <q-card-section>
          <q-input
            v-model.number="timeout"
            dense
            outlined
            type="number"
            style="max-width: 150px"
            label="Timeout (seconds)"
            stack-label
            :rules="[val => !!val || '*Required', val => val >= 5 || 'Minimum is 5 seconds']"
          />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn :loading="loading" label="Run" color="primary" type="submit" />
        </q-card-actions>
        <q-card-section v-if="ret" class="q-pl-md q-pr-md q-pt-none q-ma-none scroll" style="max-height: 50vh">
          <pre>{{ ret }}</pre>
        </q-card-section>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
// composition imports
import { ref, toRefs, onMounted } from "vue";
import { useAgentDropdown } from "@/composables/agents";
import { testScript } from "@/api/scripts";
import { useDialogPluginComponent } from "quasar";

// ui imports
import TacticalDropdown from "@/components/ui/TacticalDropdown";

export default {
  name: "TestScriptModal",
  emits: [...useDialogPluginComponent.emits],
  components: {
    TacticalDropdown,
  },
  props: {
    script: !Object,
  },
  setup(props) {
    // setup dropdowns
    const { agentOptions, getAgentOptions } = useAgentDropdown();

    // setup quasar dialog plugin
    const { dialogRef, onDialogHide } = useDialogPluginComponent();

    // make script object props single reactive properties
    const { code, default_timeout, args, shell } = toRefs(props.script);

    // main run script functionality
    const agent = ref(null);
    const ret = ref(null);
    const loading = ref(false);

    async function runTestScript() {
      loading.value = true;
      const data = {
        agent: agent.value,
        code: code.value,
        timeout: default_timeout.value,
        args: args.value,
        shell: shell.value,
      };

      ret.value = await testScript(data);
      loading.value = false;
    }

    onMounted(getAgentOptions());

    return {
      // reactive data
      agent,
      timeout: default_timeout,
      args,
      ret,
      loading,

      // non-reactive data
      agentOptions,

      // methods
      runTestScript,

      // quasar dialog plugin
      dialogRef,
      onDialogHide,
    };
  },
};
</script>