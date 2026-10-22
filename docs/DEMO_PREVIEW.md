# Demonstration preview

A **2 min 29 sec** screen recording has been produced from the actual TitaniumGuard application running locally. The application code matches the deployed prototype. It has Chinese captions, a visible cursor and highlighted controls, **with no audio**. The complete project export includes `Demo_Video/TitaniumGuard_Demo_Preview_ZH.mp4` outside the source-code folder.

This preview has not been uploaded to Devpost or a public video host. It is separate from the read-only `demo/TitaniumGuard_Demo.html` and from the English [speaking script](PITCH.md). A submitted video URL must point to the actual hosted recording; do not paste a local file path into Devpost.

## What the recording demonstrates

1. The quality engineer's problem and the synthetic data/settings.
2. A stable process: historical baseline Cpl 2.247 and no control signals.
3. A planted mean shift: 15 signal builds, with unchanged baseline limits and Cpl.
4. A stable process with insufficient margin: Cpl 0.418 and no control signals.
5. CSV import, manual entry of one complete five-coupon build, and CSV/JSON export.
6. The methods panel and the prototype's limitations.

The recording run verified the three displayed states, the filter's 15 flagged rows, the increase from 200 to 205 coupons after entry, a 205-row CSV export, and an exported JSON object matching the displayed analysis. No browser JavaScript errors were observed.

## Include the environmental plot in the final narration

In **Mean shift**, scroll below the X-bar/R charts to **Oxygen & build strength**, beside the Q-Q plot. The scatter plot has one point per build: recorded oxygen in ppm on the x-axis and mean coupon strength in MPa on the y-axis. The 15 signal builds are red. The two synthetic clusters are a planted association, not evidence of causality. See the [actual chart screenshot](images/oxygen-strength-scatter.png).

The existing preview concentrates on the control charts and workflow, so this environmental plot should be explained explicitly when preparing the final spoken demo. The English speaking script includes this step.

## Submission format

The [official criteria](https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/criteria.md) award 10 points for a clear demonstration using test datasets. They do not specify that a PPT is required. The [official README](https://github.com/timothyfraser/sixsigmahackathon/blob/main/README.md) lists no DL showcase and requires a repository link plus a demo of the working prototype. The actual Devpost form still determines any video-field or hosting requirements; a 3-minute duration is a practical speaking-script target, not a confirmed mandatory length.
