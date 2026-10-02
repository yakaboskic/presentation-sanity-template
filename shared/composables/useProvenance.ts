import { ref } from 'vue'

/**
 * Shared reactive state for the provenance panel. A single ref holds the
 * variable key currently being inspected; clicking a <DataValue> sets it,
 * the panel watches it and slides in/out.
 *
 * Module-scoped state means every importer shares the same ref — exactly
 * one panel, one selection at a time.
 */
export const provenanceKey = ref<string | null>(null)

export function showProvenance(key: string) {
  provenanceKey.value = key
}

export function hideProvenance() {
  provenanceKey.value = null
}
