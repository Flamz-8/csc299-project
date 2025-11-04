import { Meeting, MeetingCreate } from '../models/Meeting';

export class MeetingTracker {
    private meetings: Map<string, Meeting> = new Map();

    addMeeting(meetingData: MeetingCreate): Meeting {
        const id = crypto.randomUUID();
        const meeting = { ...meetingData, id };
        this.meetings.set(id, meeting);
        return meeting;
    }

    getMeeting(id: string): Meeting | undefined {
        return this.meetings.get(id);
    }

    getAllMeetings(): Meeting[] {
        return Array.from(this.meetings.values());
    }

    updateMeeting(id: string, updates: Partial<Meeting>): boolean {
        const meeting = this.meetings.get(id);
        if (!meeting) return false;
        
        this.meetings.set(id, { ...meeting, ...updates });
        return true;
    }

    deleteMeeting(id: string): boolean {
        return this.meetings.delete(id);
    }
}
