package me.cbitler.raidbot.creation;

import me.cbitler.raidbot.RaidBot;
import me.cbitler.raidbot.raids.PendingRaid;
import net.dv8tion.jda.core.events.message.priv.PrivateMessageReceivedEvent;

/**
 * Set the time for the event
 * @author Christopher Bitler
 */
public class RunTimeStep implements CreationStep {

    /**
     * Handle setting the time for the event
     * @param e The direct message event
     * @return True if the time is set, false otherwise
     */
    public boolean handleDM(PrivateMessageReceivedEvent e) {
        RaidBot bot = RaidBot.getInstance();
        PendingRaid raid = bot.getPendingRaids().get(e.getAuthor().getId());
        if (raid == null) {
        	// this will be caught in the handler
        	throw new RuntimeException();
        }

        raid.setTime(e.getMessage().getRawContent());

        return true;
    }

    /**
     * {@inheritDoc}
     */
    public String getStepText() {
        return "Enter the time for the event:";
    }

    /**
     * {@inheritDoc}
     */
    public CreationStep getNextStep() {
        return new RunOpenWorldStep();
    }
}
