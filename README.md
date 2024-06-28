# Testing the YAML Configuration

## Setup

With Valohai-CLI:

```shell
vh login --host http://{localhost}:{port}
vh project link  # <- local test project
vh yaml step hello.py  # generates the valohai.yaml file
```

### YAML Configuration

Create a `valohai.yaml` file with the following definitions
(see [valohai.yaml](./valohai.yaml)):

- step: `parse-notification`
  - Parsing step: receives the notification body with the dataset version information as input
    (in the example, input name `payload`).
  - The step outputs the dataset version URL as metadata.
- step: `list-inputs`
  - Action step; name this step according to what you do with the inputs.
  - This step receives the dataset version URL as a parameter.
  - The parameter value is passed to an input (e.g. `dataset`).
- pipeline: `Dataset handling automation`
  - Give the pipeline a descriptive name; this is used in the trigger action to run the pipeline.
  - Connect the parsing step output metadata to the action step parameter.

You can name steps and parameters however you like;
just remember to use the correct names in the following setup.

## Setup on Valohai

_Note: this is the updated documentation for using a notification trigger
instead of the old workflow that used a webhook._

### 1. Create Project

Create a project that is owned by an organization
(notification triggers don’t work on personal projects).

### 2. Create Trigger

Go to _Settings_ > _Triggers_ > _Create trigger_.

Set the trigger values:

- Title: descriptive title, e.g. `Dataset version -> new data handler pipeline`
- Trigger type: `Notification`
- Actions: `Run Pipeline`
  - Source Commit Reference: `main` (or e.g. a reference to a specific commit)
  - Pipeline Name: `Dataset handling automation` (the name used in the `valohai.yaml` file)
  - Pipeline Title: (the title for the pipeline runs created by this trigger)
  - Payload input name: `parse-notification.payload` (step and input names from `valohai.yaml`)

A _Managed Trigger Channel_ notification channel is automatically created for you
when you save the trigger.

### 3. Create Project Notification

Go to _Settings_ > _Notifications_ > _Project Notifications_ > _Create new notification routing_.

- Event: `dataset version is created`
- Filter events by users: `All users`
- Channel: select the `Launches trigger: TRIGGER_TITLE` channel (for the trigger you just created).

## Testing

You can test the actions bit by bit (locally or on Valohai).
For local testing: the following components need to be running:

- Roi (manage: `runserver`)
- Roi workers (manage: `roi_worker`)
- Peon (queue `work`)

### Parsing Notification Step

You can test parsing the notification payload manually.

Create a payload input file and add it to your project.
A minimal example of the payload file:

```json
{
  "type": "dataset_version_created",
  "data": {
    "version":{
      "uri": "DATASET_VERSION_URL"
    }
  }
}
```

1. Create a new execution:
2. Select the `parse-notification` step.
3. Add the payload input file as the execution input.
4. Run the execution.
5. The dataset version URL is printed out in the execution log.
6. The execution metadata includes a list of files in the dataset version.

You can also run the step from the command line
by giving a valid payload file URL as input:

```shell
vh execution run --adhoc parse-notification --payload="datum://01903653-c618-3562-ffa1-8ecdf2eefd06"
```

### Handling Inputs Step

The input handler step requires a dataset version URL as input.

1. Create a dataset.
2. Create a new dataset and add files to it.
3. Go to _Executions_ > _Create execution_.
4. Select the action step.
5. Paste the dataset version datum URL into the _Data_ > _Inputs_ > your step input > _URL_ field.
6. Set the _dataset_url_ parameter to an empty string (`""`).
7. Run the execution.

Command line: give a dataset version URL as parameter:

```shell
vh execution run --adhoc list-inputs --dataset-url="dataset://trigger-test/trigger-test-two-files"
```

### Triggering Pipeline

You cannot pass inputs to a pipeline node from the command line,
so to run the pipeline from the CLI,
you need to set a default payload input for the parsing step in the YAML configuration.

After that, you can run the pipeline with,

```shell
vh pipeline run --adhoc "Dataset handling automation"
```
