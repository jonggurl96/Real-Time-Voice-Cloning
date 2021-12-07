# from encoder.visualizations import Visualizations
from encoder.data_objects import SpeakerVerificationDataLoader, SpeakerVerificationDataset
from encoder.params_model import *
from encoder.model import SpeakerEncoder
# from utils.profiler import Profiler
from pathlib import Path
from tqdm import tqdm
import torch
import sys

def sync(device: torch.device):
    # For correct profiling (cuda operations are async)
    if device.type == "cuda":
        torch.cuda.synchronize(device)
    
def _save_model(save_path: Path, step, model, optimizer):
    torch.save({
        "step": step + 1,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
    }, save_path)
    
def train(run_id: str, clean_data_root: Path, models_dir: Path, umap_every: int, save_every: int,
          backup_every: int, vis_every: int, force_restart: bool, visdom_server: str,
          no_visdom: bool):
    
    # Create a dataset and a dataloader
    dataset = SpeakerVerificationDataset(clean_data_root)
    loader = SpeakerVerificationDataLoader(
        dataset,
        speakers_per_batch, # batch 당 64speaker
        utterances_per_speaker, # speaker 당 최대 10개 대화
        num_workers=8,
    )
    
    # Setup the device on which to run the forward pass and the loss. These can be different, 
    # because the forward pass is faster on the GPU whereas the loss is often (depending on your
    # hyperparameters) faster on the CPU.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # FIXME: currently, the gradient is None if loss_device is cuda
    loss_device = torch.device("cpu")
    
    # Create the model and the optimizer
    model = SpeakerEncoder(device, loss_device)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate_init)
    init_step = 1
    
    # Configure file path for the model
    state_fpath = models_dir.joinpath(run_id + ".pt")
    backup_dir = models_dir.joinpath(run_id + "_backups")
    optim_dir = models_dir.joinpath(run_id + "_optim.pt")

    # Load any existing model
    if not force_restart:
        if state_fpath.exists():
            print("Found existing model \"%s\", loading it and resuming training." % run_id)
            checkpoint = torch.load(state_fpath)
            init_step = checkpoint["step"]
            model.load_state_dict(checkpoint["model_state"])
            optimizer.load_state_dict(checkpoint["optimizer_state"])
            optimizer.param_groups[0]["lr"] = learning_rate_init
        else:
            print("No model \"%s\" found, starting training from scratch." % run_id)
    else:
        print("Starting the training from scratch.")
    model.train()
    
    # Initialize the visualization environment
    # vis = Visualizations(run_id, vis_every, server=visdom_server, disabled=no_visdom)
    # vis.log_dataset(dataset)
    # vis.log_params()
    device_name = str(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
    # vis.log_implementation({"Device": device_name})
    
    # Training loop
    # profiler = Profiler(summarize_every=10, disabled=False)
    print(device_name)
    max_loss = 9.99
    for step, speaker_batch in enumerate(loader, init_step):
        # profiler.tick("Blocking, waiting for batch (threaded)")
        
        # Forward pass
        inputs = torch.from_numpy(speaker_batch.data).to(device)
        sync(device)
        # profiler.tick("Data to %s" % device)
        embeds = model(inputs)
        sync(device)
        embeds_loss = embeds.view((speakers_per_batch, utterances_per_speaker, -1)).to(loss_device)
        loss, eer = model.loss(embeds_loss)
        sync(loss_device)
        # profiler.tick("Loss")

        # Backward pass
        model.zero_grad()
        loss.backward()
        # profiler.tick("Backward pass")
        model.do_gradient_ops()
        optimizer.step()
        # profiler.tick("Parameter update")
        
        # Update visualizations
        # learning_rate = optimizer.param_groups[0]["lr"]
        # vis.update(loss.item(), eer, step)
        
        msg = f"step: {step}, loss: {loss:.6f}"
        
        # Draw projections and save them to the backup folder
        if umap_every != 0 and step % umap_every == 0:
            msg = msg + ", Drawing and saving projections (step %d)" % step
            backup_dir.mkdir(exist_ok=True)
            projection_fpath = backup_dir.joinpath("%s_umap_%06d.png" % (run_id, step))
            embeds = embeds.detach().cpu().numpy()
            # vis.draw_projections(embeds, utterances_per_speaker, step, projection_fpath)
            # vis.save()

        # Overwrite the latest version of the model
        if save_every != 0 and step % save_every == 0:
            msg = msg + ", Saving the model (step %d)" % step
            torch.save({
                "step": step + 1,
                "model_state": model.state_dict(),
                "optimizer_state": optimizer.state_dict(),
            }, state_fpath)
            
        # Make a backup
        if backup_every != 0 and step % backup_every == 0:
            msg = msg + ", Making a backup (step %d)" % step
            backup_dir.mkdir(exist_ok=True)
            backup_fpath = backup_dir.joinpath("%s_bak_%06d.pt" % (run_id, step))
            _save_model(backup_fpath, step, model, optimizer)
            
        # Save lowest loss model state
        if max_loss > loss:
            max_loss = loss
            _save_model(optim_dir, step, model, optimizer)
            msg = "Save Model " + msg + "\n"
        
        sys.stdout.write("\r%s" % msg)
            
        # profiler.tick("Extras (visualizations, saving)")
