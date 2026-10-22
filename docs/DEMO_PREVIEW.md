# Demonstration preview

A **2 min 29 sec** screen recording has been produced from the actual TitaniumGuard application running locally. The application code matches the deployed prototype. It has English captions, a visible cursor and highlighted controls, **with no audio**. The English-captioned recording is named `TitaniumGuard_Demo_EN.mp4` and is provided separately from the source-code repository.

A public hosting URL and completed Devpost submission have not yet been verified. It is separate from the read-only `demo/TitaniumGuard_Demo.html` and from the English [speaking script](PITCH.md). A submitted video URL must point to the actual hosted recording; do not paste a local file path into Devpost.

## What the recording demonstrates

1. The quality engineer's problem and the synthetic data/settings.
2. A stable process: historical baseline Cpl 2.247 and no control signals.
3. A planted mean shift: 15 signal builds, with unchanged baseline limits and Cpl.
4. A stable process with insufficient margin: Cpl 0.418 and no control signals.
5. CSV import, manual entry of one complete five-coupon build, and CSV/JSON export.
6. The methods panel and the prototype's limitations.

The recording run verified the three displayed states, the filter's 15 flagged rows, the increase from 200 to 205 coupons after entry, a 205-row CSV export, and an exported JSON object matching the displayed analysis. No browser JavaScript errors were observed.

## Additional environmental context

In **Mean shift**, scroll below the X-bar/R charts to **Oxygen & build strength**, beside the Q-Q plot. The scatter plot has one point per build: recorded oxygen in ppm on the x-axis and mean coupon strength in MPa on the y-axis. The 15 signal builds are red. The two synthetic clusters are a planted association, not evidence of causality. See the [actual chart screenshot](images/oxygen-strength-scatter.png).

The recording concentrates on the control charts and workflow; it does not provide a dedicated explanation of this scatter plot. The linked screenshot, project description and walkthrough document that feature. The optional speaking script includes it for anyone choosing to record a narrated version.

## Submission format

The [official criteria](https://github.com/timothyfraser/sixsigmahackathon/blob/main/docs/criteria.md) award 10 points for a clear demonstration using test datasets. They do not specify that a PPT is required. The [official README](https://github.com/timothyfraser/sixsigmahackathon/blob/main/README.md) lists no DL showcase and requires a repository link plus a demo of the working prototype. No narration or on-camera requirement was found in the reviewed public rules. A 3-minute duration is an optional speaking-script target, not a mandatory length. The actual submission form controls its required fields.

## Upload to YouTube and add the link to Devpost

1. Upload **`TitaniumGuard_Demo_EN.mp4`**, the English-captioned version.
2. Set visibility to **Public** or **Unlisted**, not Private. Unlisted videos are viewable by anyone with the link without a Google account.
3. Wait for video processing, then open the viewing link in a signed-out or private browser window and confirm that the image and captions are readable.
4. Paste the viewing URL into the hackathon submission's **Video demo link** field. Confirm that it plays in the Devpost preview.
5. Complete the hackathon submission and retain its confirmation. Uploading to YouTube alone does not submit the project.

Devpost notes that a project page and its hackathon submission can have different video links; check the video attached to this submission. Sources: [Devpost video instructions](https://help.devpost.com/article/85-uploading-a-demo-video) and [YouTube visibility](https://support.google.com/youtube/answer/157177).
