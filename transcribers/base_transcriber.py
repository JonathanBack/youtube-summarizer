"""Base class for transcript acquisition."""

from abc import ABC, abstractmethod


class BaseTranscriber(ABC):
    """Abstract base class for all transcribers.

    Defines the common interface for getting transcripts.
    """

    @abstractmethod
    def get_transcript(self, video_url: str) -> list:
        """Get transcript for a video.

        Args:
            video_url (str): URL of the video

        Returns:
            list: List of transcript segments with timing information

        """
        pass
