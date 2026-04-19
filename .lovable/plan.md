
Investigating: User clicks "View Reproducibility Score" → 404. Per memory, the separate ReproducibilityScore page was consolidated into FixPreview.tsx as a collapsible section. So the link likely still points to an old route like `/reproducibility-score` that no longer exists.

Need to find where the "View Reproducibility Score" button/link lives and fix its target.
