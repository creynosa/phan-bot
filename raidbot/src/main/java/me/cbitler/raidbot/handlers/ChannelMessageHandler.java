package me.cbitler.raidbot.handlers;

import me.cbitler.raidbot.RaidBot;
import me.cbitler.raidbot.commands.Command;
import me.cbitler.raidbot.commands.CommandRegistry;
import me.cbitler.raidbot.creation.CreationStep;
import me.cbitler.raidbot.creation.RunNameStep;
import me.cbitler.raidbot.edit.EditStep;
import me.cbitler.raidbot.edit.EditIdleStep;
import me.cbitler.raidbot.raids.Raid;
import me.cbitler.raidbot.raids.RaidManager;
import me.cbitler.raidbot.utility.PermissionsUtil;
import me.cbitler.raidbot.utility.RoleTemplates;
import net.dv8tion.jda.core.Permission;
import net.dv8tion.jda.core.events.message.guild.GuildMessageDeleteEvent;
import net.dv8tion.jda.core.events.message.guild.GuildMessageReceivedEvent;
import net.dv8tion.jda.core.hooks.ListenerAdapter;

/**
 * Handle channel message-related events sent to the bot
 * @author Christopher Bitler
 * @author Franziska Mueller
 */
public class ChannelMessageHandler extends ListenerAdapter {

    /**
     * Handle receiving a message. This checks to see if it matches the !createEvent or !removeFromEvent commands
     * and acts on them accordingly.
     *
     * @param e The event
     */
    @Override
    public void onGuildMessageReceived(GuildMessageReceivedEvent e) {
        RaidBot bot = RaidBot.getInstance();
        if (e.getAuthor().isBot()) {
           return;
        }

        if(e.getMessage().getRawContent().startsWith("!")) {
            String[] messageParts = e.getMessage().getRawContent().split(" ");
            String[] arguments = CommandRegistry.getArguments(messageParts);
            Command command = CommandRegistry.getCommand(messageParts[0].replace("!",""));
            if(command != null) {
                command.handleCommand(messageParts[0], arguments, e.getChannel(), e.getAuthor());

                try {
                    e.getMessage().delete().queue();
                } catch (Exception exception) {}
            }
        }
        
        if (PermissionsUtil.hasRaidLeaderRole(e.getMember())) {
            if (e.getMessage().getRawContent().equalsIgnoreCase("!createEvent")) {
            	// check if this user already has an active chat
            	int actvId = bot.userHasActiveChat(e.getAuthor().getId());
    			if (actvId != 0) {
    				RaidBot.writeNotificationActiveChat(e.getAuthor(), actvId);
    				try {
                        e.getMessage().delete().queue();
                    } catch (Exception exception) {}
    				return;
    			}
            	CreationStep runNameStep = new RunNameStep(e.getMessage().getGuild().getId());
            	e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage(runNameStep.getStepText()).queue());
            	bot.getCreationMap().put(e.getAuthor().getId(), runNameStep);
            	try {
                    e.getMessage().delete().queue();
                } catch (Exception exception) {}
            } else if (e.getMessage().getRawContent().toLowerCase().startsWith("!removefromevent")) {
                String[] split = e.getMessage().getRawContent().split(" ");
                if(split.length < 3) {
                    e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Format for !removeFromEvent: !removeFromEvent [event id] [name]").queue());
                } else {
                    String messageId = split[1];
                    String name = split[2];

                    Raid raid = RaidManager.getRaid(messageId);

                    if (raid != null && raid.getServerId().equalsIgnoreCase(e.getGuild().getId())) {
                        raid.removeUserByName(name);
                    } else {
                        e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Non-existant event.").queue());
                    }
                }
                try {
                    e.getMessage().delete().queue();
                } catch (Exception exception) {}
            } 
        }
        
        // edit can be made by event managers or the leader of the event (enables fractal event editing)
        if (e.getMessage().getRawContent().toLowerCase().startsWith("!editevent")) {
           	String[] split = e.getMessage().getRawContent().split(" ");
            if(split.length < 2) {
                e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Format for !editEvent: !editEvent [event id]").queue());
            } else {
                String messageId = split[1];
                Raid raid = RaidManager.getRaid(messageId);
                if (raid != null && raid.getServerId().equalsIgnoreCase(e.getGuild().getId())) {
                	// check permissions here since raid leader should also be able to edit
                    if (PermissionsUtil.hasRaidLeaderRole(e.getMember()) || e.getAuthor().getId().contentEquals(raid.getRaidLeaderId())) {
                    	// check if this user already has an active chat
                    	int actvId = bot.userHasActiveChat(e.getAuthor().getId());
            			if (actvId != 0) {
            				RaidBot.writeNotificationActiveChat(e.getAuthor(), actvId);
            				try {
                                e.getMessage().delete().queue();
                            } catch (Exception exception) {}
            				return;
            			}
                    	// check if the raid is being edited by someone else
                    	if (bot.getEditList().contains(messageId)) {
                    		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("The selected event is already being edited.").queue());
                    	} else {
                    		// start editing process
                    		EditStep editIdleStep = new EditIdleStep(messageId);
                    		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage(editIdleStep.getStepText()).queue());
                    		bot.getEditMap().put(e.getAuthor().getId(), editIdleStep);
                    		bot.getEditList().add(messageId);
                    	}
                    } 
                } else {
                    e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Non-existant event.").queue());
                }
            }
            try {
                e.getMessage().delete().queue();
            } catch (Exception exception) {}
        }

        // all commands that require manage server permissions
        if (e.getMember().getPermissions().contains(Permission.MANAGE_SERVER)) {
        	boolean setEventManager = e.getMessage().getRawContent().toLowerCase().startsWith("!seteventmanagerrole");
        	boolean setFractalCreator = e.getMessage().getRawContent().toLowerCase().startsWith("!setfractalcreatorrole");
        	boolean setFractalChannel = e.getMessage().getRawContent().toLowerCase().startsWith("!setfractalchannel");
        	boolean setArchiveChannel = e.getMessage().getRawContent().toLowerCase().startsWith("!setarchivechannel");
            if (setEventManager || setFractalCreator || setFractalChannel || setArchiveChannel) {
                String[] commandParts = e.getMessage().getRawContent().split(" ");
                String specifiedName = combineArguments(commandParts,1);
                if (setEventManager) {
                	RaidBot.getInstance().setRaidLeaderRole(e.getMember().getGuild().getId(), specifiedName);
                	e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Event manager role updated to: " + specifiedName).queue());
                } else if (setFractalCreator) {
                	RaidBot.getInstance().setFractalCreatorRole(e.getMember().getGuild().getId(), specifiedName);
                	e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Fractal creator role updated to: " + specifiedName).queue());
                } else if (setFractalChannel) {
                	if (RaidBot.getInstance().setFractalChannel(e.getMember().getGuild().getId(), specifiedName)) {
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Fractal announcement channel updated to: " + specifiedName).queue());
                	} else {
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Invalid channel name.").queue());
                	}
                } else if (setArchiveChannel) {
                	int success = RaidBot.getInstance().setArchiveChannel(e.getMember().getGuild().getId(), specifiedName);
                	if (success == 0) {
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Archive channel successfully updated to *" + specifiedName + "*.").queue());
                	} else if (success == 1){
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("The channel *" + specifiedName + "* does not exist on this server.").queue());
                	} else if (success == 2) {
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("I do not have write permissions to the channel *" + specifiedName + "*.").queue());
                	}
                }
                try {
                    e.getMessage().delete().queue();
                } catch (Exception exception) {}
            }
        }
        
        // new creation command for fractal event
        if (PermissionsUtil.hasRaidLeaderRole(e.getMember()) || PermissionsUtil.hasFractalCreatorRole(e.getMember())) {
        	String createFracCommand = "!createfractal";
            if (e.getMessage().getRawContent().toLowerCase().startsWith(createFracCommand)) {
            	String[] split = new String[0];
            	try {
            		split = e.getMessage().getRawContent().substring(createFracCommand.length()+1).split(";");
            	} catch (Exception excp) { }
            	String helpMessageAccum = "Correct format: !createFractal [name];[date];[time];[team comp id]\n"
            			+ "Enter the information without brackets, for example: !createFractal CMs+T4;13.04.19;13:37 CEST;1\n"
            			+ "Available team compositions:\n";
            	String[] templNames = RoleTemplates.getFractalTemplateNames();
            	for (int t = 0; t < templNames.length; t++) {
            		helpMessageAccum += "`" + (t+1) + "` " + RoleTemplates.templateToString(templNames[t], RoleTemplates.getFractalTemplates()[t]) + "\n";
            	}
            	String helpMessage = helpMessageAccum; // otherwise the lambda for sending the message is unhappy because var not effectively final
                
                if(split.length < 4) {
            		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Incorrect number of arguments provided.").queue());
                    e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage(helpMessage).queue());
                } else { 
                	// check if the team comp is valid
                	boolean validTeamComp = true;
                	int teamCompId = -1;
                	try {
                		teamCompId = Integer.parseInt(split[3]) - 1;
                	} catch (Exception excp) {
                		validTeamComp = false;
                	}
                	if (teamCompId >= RoleTemplates.getFractalTemplateNames().length)
                		validTeamComp = false;
                	if (validTeamComp == false) {
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage("Provided team comp id is invalid.").queue());
                		e.getAuthor().openPrivateChannel().queue(privateChannel -> privateChannel.sendMessage(helpMessage).queue());
                	} else {
                		String name = split[0];
                		String date = split[1];
                		String time = split[2];
                		// create fractal event
                		RaidManager.createFractal(e.getAuthor(), e.getGuild().getId(), name, date, time, teamCompId);
                	}
                }
                try {
                    e.getMessage().delete().queue();
                } catch (Exception exception) {}
            }
        }
    }

    @Override
    public void onGuildMessageDelete(GuildMessageDeleteEvent e) {
    	Raid raid = RaidManager.getRaid(e.getMessageId()); 
        if (raid != null && raid.getServerId().equalsIgnoreCase(e.getGuild().getId())) {
        	raid.postToArchive();
            RaidManager.deleteRaid(e.getMessageId(), true);
        }
    }

    /**
     * Combine the strings in an array of strings
     * @param parts The array of strings
     * @param offset The offset in the array to start at
     * @return The combined string
     */
    private String combineArguments(String[] parts, int offset) {
        String text = "";
        for (int i = offset; i < parts.length; i++) {
            text += (parts[i] + " ");
        }

        return text.trim();
    }
}
